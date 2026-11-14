# Kings enquiry delivery — prepared, not activated

Destination for every form: kingsofkingsinternational@gmail.com.
Automated acknowledgement From: no-reply@kingsofkingsinternational.com.
The public website never displays the destination address. It sends a JSON POST to /api/enquiries when deployed. The local preview only validates the form and reports that nothing was sent or registered.

The prepared Python transport in enquiries.py validates fields, sends the enquiry with the sender as Reply-To, then sends an automatic receipt from the domain address. A confirmation failure is distinguished from failure to deliver the enquiry. No password is stored in these files. This transport has not been connected to a public HTTP endpoint.

At hosting setup:
- Create/authorize no-reply and select an authenticated SMTP service. Configure SPF, DKIM and DMARC for the real mail provider.
- Keep enquiries.py outside the public document root. Implement the POST endpoint with a request-size limit, same-origin checks, server-side validation, rate limits and bot protection. Use HTTPS and exclude submissions from public logs. Never send form payloads to an AI service without the user's approved handling policy.
- Set KOK_MAIL_ENABLED=yes and KOK_SMTP_HOST, KOK_SMTP_PORT, KOK_SMTP_USER, KOK_SMTP_PASSWORD in private environment configuration.
- Test delivery to Gmail, Reply-To, automated receipts, failure handling and spam placement before enabling public submissions. Change Review enquiry to Send enquiry and remove the preview note only when the real endpoint is verified.
- Connect mailing opt-ins to a proper subscription store and verified unsubscribe handling. Forms currently prepare requests; no mailing-list platform or database is connected.
- Configure an agent on the receiving mailbox separately. Automatic replies and forwarding to Colin are not activated; Colin's destination address has not been supplied. Approve that workflow and its access before enabling it.
- Giveaway entries remain closed pending eligibility, deadline, final prize specification and official rules. Notification requests are not entries and do not require unrelated marketing consent.
- Revise privacy text to reflect actual hosting, enquiry handling, retention and providers before launch.
