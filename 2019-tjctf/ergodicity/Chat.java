package com.chatserver;

import com.chatserver.util.HerokuUtil;
import com.chatserver.util.AES;

import java.util.Base64;
import io.javalin.Javalin;
import io.javalin.websocket.WsSession;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.eclipse.jetty.websocket.api.Session;
import org.json.JSONObject;
import java.util.Random;
import java.util.Arrays;
import javax.xml.bind.DatatypeConverter;
import java.nio.charset.StandardCharsets;
import static j2html.TagCreator.article;
import static j2html.TagCreator.attrs;
import static j2html.TagCreator.b;
import static j2html.TagCreator.p;
import static j2html.TagCreator.span;

public class Chat {

    private static Map<WsSession, String> userUsernameMap = new ConcurrentHashMap<>();
    private static Map<String, AES> userCiphers = new ConcurrentHashMap<>();
    private static int nextUserNumber = 1;

    public static void main(String[] args) {
        Javalin.create()
            .port(HerokuUtil.getHerokuAssignedPort())
            .enableStaticFiles("/public")
            .ws("/chat", ws -> {
                ws.onConnect(session -> {
                    String username = "User" + nextUserNumber++;
                    userUsernameMap.put(session, username);
                    long timestamp = ((long) System.currentTimeMillis() / 1000);
                    Random random = new Random(timestamp);
                    String key  = String.format("%016x", ((long)(random.nextDouble()*10000000000L)));
                    String ivec  = String.format("%016x", ((long)(random.nextDouble()*10000000000L)));
                    AES cipher = new AES(key.getBytes("UTF-8"), ivec.getBytes("UTF-8"), "AES/CBC/PKCS5PADDING");
                    userCiphers.put(username, cipher);
                    broadcastMessage("Server", (username + " joined the chat."));
                });
                ws.onClose((session, status, message) -> {
                    String username = userUsernameMap.get(session);
                    userUsernameMap.remove(session);
                    broadcastMessage("Server", (username + " left the chat"));
                });
                ws.onMessage((session, message) -> {
                    broadcastMessage(userUsernameMap.get(session), message);
                });
            })
            .start();
    }

    private static void broadcastMessage(String sender, String message) {
        userUsernameMap.keySet().stream().filter(Session::isOpen).forEach(session -> {
            if(!sender.startsWith("Server")) {
              String username = userUsernameMap.get(session);
              AES cipher = userCiphers.get(username);
              byte[] encrypted = cipher.encrypt(createHtmlMessageFromSender(sender, message));
              cipher.updateIV(encrypted);
              String encoded = Base64.getEncoder().encodeToString(encrypted);
              session.send(
                  new JSONObject()
                      .put("userMessage", encoded)
                      .put("userlist", userUsernameMap.values()).toString()
              );
            } else {
              session.send(
                  new JSONObject()
                      .put("userMessage", createHtmlMessageFromSender(sender, message))
                      .put("userlist", userUsernameMap.values()).toString()
              );
            }
        });
    }

    private static String createHtmlMessageFromSender(String sender, String message) {
        if(sender.startsWith("Server")) {
          return article(
              b(sender + " says:"),
              p(message)
          ).render();
        } else {
          return article(
              b(sender + " says:"),
              span(attrs(".timestamp"), new SimpleDateFormat("HH:mm:ss").format(new Date())),
              p(message)
          ).render();
        }
    }
}
