import logging

import pytest

from flask_graphite import (DEFAULT_GROUP, DEFAULT_HOST, DEFAULT_PORT,
                            FlaskGraphite)


@pytest.fixture
def plugin():
    return FlaskGraphite()


def test_init(app):
    FlaskGraphite(app)


def test_init_app(app, plugin):
    plugin.init_app(app)


def test_init_failed(caplog, app, plugin):
    caplog.set_level(logging.ERROR)
    app.config["FLASK_GRAPHITE_DRYRUN"] = False
    plugin.init_app(app)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"


def test_default_config(app, plugin):
    app.config["FLASK_GRAPHITE_DRYRUN"] = True  # To not raise error
    plugin.init_app(app)
    assert app in plugin.config
    assert plugin.config[app]["graphite_server"] == DEFAULT_HOST
    assert plugin.config[app]["graphite_port"] == DEFAULT_PORT
    assert plugin.config[app]["group"] == DEFAULT_GROUP
    assert plugin.config[app]["autoreconnect"] is True


def test_config(app, plugin):
    app.config["FLASK_GRAPHITE_HOST"] = "google.com"
    app.config["FLASK_GRAPHITE_PORT"] = 1337
    app.config["FLASK_GRAPHITE_DRYRUN"] = True
    plugin.init_app(app)
    assert app in plugin.config
    assert plugin.config[app]["graphite_server"] == "google.com"
    assert plugin.config[app]["graphite_port"] == 1337
    assert plugin.config[app]["dryrun"] is True


def test_setup_graphitesend(app, plugin):
    app.config["FLASK_GRAPHITE_DRYRUN"] = True
    app.config["FLASK_GRAPHITE_AUTORECONNECT"] = True
    plugin.init_app(app)
    assert app.graphite.dryrun is True
    assert app.graphite._autoreconnect is True
