# apli-feedback-form
This is with regards to the assignment provided by Apli.ai for internship opportunities.

This Django webapp has a single sub application `feedback`, which portrays the functioning of a feedback gathering form.

The form has 5 fields,
1. username
2. email
3. subject
4. message (Markdown)
5. image (Optional)

On the front-end side, the form,
* exhibits a "reCAPTCHA" feature along with the provided 5 data fields.
* has proper styling for error messages if any.
* has an embedded and expandable [summernote][summernote] markdown editor.

[summernote]: https://summernote.org/
* has various placeholders and help texts for user guidance.

On the back-end side, the form,
* supports multiple images to be embedded in a single feedback for any changes, in future.
* has auto-filled `username` and `email` for authenticated users.
* has username check, for unregistered users.
* has double check on size of the image to be uploaded, first at form level and then at model level.
* sends 'html' emails to users and operations team, operations team gets the attached image along with feedback data.
* extension validator is employed at model level.

Along with this, App also has comprehensive automated tests.

All the settings regarding the Emails and summernote editor are available in
[settings][settings].

[settings]: https://github.com/manthanchauhan/apli-feedback-form/blob/3493099f839a7de4f8cdeb78fcc985ca896edc63/apli_ai/apli_ai/settings.py#L131-L159