from mimeo.utils.renderers import UtilsRenderer


def test_phone_raw():
    phone = UtilsRenderer.render_raw("phone")
    assert isinstance(phone, str)
    assert len(phone) == 12
    assert phone.replace("-", "").isnumeric()


def test_phone_parametrized_default():
    mimeo_util = {"_name": "phone"}
    phone = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(phone, str)
    assert len(phone) == 12
    assert phone.replace("-", "").isnumeric()
