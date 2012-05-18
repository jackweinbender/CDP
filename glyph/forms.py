from flaskext.wtf import Form, Required, TextAreaField, RadioField, HiddenField, validators


class RecordForm(Form):
    record = TextAreaField(u"Record Text",
    [Required(
        u"Record Text"),
        validators.length(max=50,
            message=u"Please use 50 characters or less")])
