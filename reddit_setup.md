# Reddit Bot Credential Setup

1. Click on this link to begin: [Reddit Application Creation](https://www.reddit.com/prefs/apps)
2. Login in to your Reddit account, if not already logged in
3. Select `are you a developer? create an app...`
4. You will be prompted to fill in a couple of fields, which will be discussed in the next steps

![Create Application Page](images/create_application_page.png)

5. Fill in the field for `name` (can be anything)
6. Select `web app`
7. Fill in the field for `description` (can be anything) 
8. Fill in the fields for `about url` and `redirect url` (can be anything). If any error occurs, ensure 'https://' is at the beginning of your link.
9. Select `Create App`
10. You will see the following page

![Reddit Developer Application](images/reddit_developer_application.png)

11. Based on the above image, save your `CLIENT_ID` and `CLIENT_SECRET`
12. Open secret.py
13. Fill in the respective values for `CLIENT_ID`and `CLIENT_SECRET`. The value for `USER_AGENT` can be any value you desire
14. Save secret.py