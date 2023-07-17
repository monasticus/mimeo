from mimeo.utils.renderers import UtilsRenderer


def test_phone_raw():
    phone = UtilsRenderer.render_raw("phone")
    assert isinstance(phone, str)
    assert len(phone) == 12
    assert phone[0].isnumeric()
    assert phone[1].isnumeric()
    assert phone[2].isnumeric()
    assert phone[3] == "-"
    assert phone[4].isnumeric()
    assert phone[5].isnumeric()
    assert phone[6].isnumeric()
    assert phone[7] == "-"
    assert phone[8].isnumeric()
    assert phone[9].isnumeric()
    assert phone[10].isnumeric()
    assert phone[11].isnumeric()


def test_phone_parametrized_default():
    mimeo_util = {"_name": "phone"}
    phone = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(phone, str)
    assert len(phone) == 12
    assert phone[0].isnumeric()
    assert phone[1].isnumeric()
    assert phone[2].isnumeric()
    assert phone[3] == "-"
    assert phone[4].isnumeric()
    assert phone[5].isnumeric()
    assert phone[6].isnumeric()
    assert phone[7] == "-"
    assert phone[8].isnumeric()
    assert phone[9].isnumeric()
    assert phone[10].isnumeric()
    assert phone[11].isnumeric()


def test_phone_parametrized_custom_uppercase():
    mimeo_util = {"_name": "phone", "format": "(+XX) XXX XXX XXX"}
    phone = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(phone, str)
    assert len(phone) == 17
    assert phone[0] == "("
    assert phone[1] == "+"
    assert phone[2].isnumeric()
    assert phone[3].isnumeric()
    assert phone[4] == ")"
    assert phone[5] == " "
    assert phone[6].isnumeric()
    assert phone[7].isnumeric()
    assert phone[8].isnumeric()
    assert phone[9] == " "
    assert phone[10].isnumeric()
    assert phone[11].isnumeric()
    assert phone[12].isnumeric()
    assert phone[13] == " "
    assert phone[14].isnumeric()
    assert phone[15].isnumeric()
    assert phone[16].isnumeric()


def test_phone_parametrized_custom_lowercase():
    mimeo_util = {"_name": "phone", "format": "(+xx) xxx xxx xxx"}
    phone = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(phone, str)
    assert len(phone) == 17
    assert phone[0] == "("
    assert phone[1] == "+"
    assert phone[2].isnumeric()
    assert phone[3].isnumeric()
    assert phone[4] == ")"
    assert phone[5] == " "
    assert phone[6].isnumeric()
    assert phone[7].isnumeric()
    assert phone[8].isnumeric()
    assert phone[9] == " "
    assert phone[10].isnumeric()
    assert phone[11].isnumeric()
    assert phone[12].isnumeric()
    assert phone[13] == " "
    assert phone[14].isnumeric()
    assert phone[15].isnumeric()
    assert phone[16].isnumeric()


def test_phone_parametrized_with_format_with_no_placeholders():
    mimeo_util = {"_name": "phone", "format": "No placeholder"}
    phone = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(phone, str)
    assert phone == "No placeholder"
