from flask import jsonify, render_template, Blueprint
from apispec import APISpec
from apispec.exceptions import APISpecError
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


class FlaskRestfulPlugin(FlaskPlugin):
    """Small plugin override to handle flask-restful resources"""

    @staticmethod
    def _rule_for_view(view, app=None):
        view_funcs = app.view_functions
        endpoint = None

        for ept, view_func in view_funcs.items():
            if hasattr(view_func, "view_class"):
                view_func = view_func.view_class

            if view_func == view:
                endpoint = ept

        if not endpoint:
            raise APISpecError("Could not find endpoint for view {0}".format(view))

        # WARNING: Assume 1 rule per view function for now
        rule = app.url_map._rules_by_endpoint[endpoint][0]
        return rule


class APISpecExt:
    """Very simple and small extension to use apispec with this API as a flask extension"""

    def __init__(self, app=None, **kwargs):
        self.spec = None

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app.config.setdefault("APISPEC_TITLE", "Quotes API")
        app.config.setdefault("APISPEC_VERSION", "v1.0.0")
        app.config.setdefault("OPENAPI_VERSION", "3.0.2")
        app.config.setdefault("SWAGGER_JSON_URL", "/swagger.json")
        app.config.setdefault("SWAGGER_UI_URL", "/swagger")
        app.config.setdefault("SWAGGER_URL_PREFIX", None)

        info_object = {
            "description": "**Quotes API** is a *REST API* that offers access to its feature rich platform. Serve some of the most **famous quotes** from all time. This is an interactive API documentation, feel free to try it out.",
            "contact": {
                "name": "Miguel Osuna",
                "url": "https://www.miguel-osuna.com",
                "email": "contact@miguel-osuna.com",
            },
        }

        tag_object = [
            {"name": "Quote", "description": "Access to quote service."},
            {"name": "Author", "description": "Access to author service."},
            {"name": "Tag", "description": "Access to tag service."},
            {"name": "User", "description": "Access to user service."},
            {
                "name": "Authentication",
                "description": "Access to authentication service.",
            },
        ]

        server_object = [{"url": app.config["SERVER"]}]

        self.spec = APISpec(
            title=app.config["APISPEC_TITLE"],
            version=app.config["APISPEC_VERSION"],
            openapi_version=app.config["OPENAPI_VERSION"],
            plugins=[MarshmallowPlugin(), FlaskRestfulPlugin()],
            **kwargs,
            info=info_object,
            tags=tag_object,
            servers=server_object
        )

        blueprint = Blueprint(
            "swagger",
            __name__,
            template_folder="./templates",
            url_prefix=app.config["SWAGGER_URL_PREFIX"],
        )

        @blueprint.route("/swagger.json")
        def swagger_json():
            return jsonify(self.spec.to_dict())

        @blueprint.route("/documentation")
        def swagger_ui():
            return render_template("swagger.j2")

        app.register_blueprint(blueprint)
