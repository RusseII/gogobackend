# workshop
Workshop - How to make and host a website

The purpose of this workshop is to learn how to build and host a simple website.
For this workshop we will be making a webserver using python and flask. This webserver 
will host and serve all of your files.

To allow other people to see your website we will use a service called ngrok.
ngrok is very useful for allowing people to quickly access your website for testing,
however for actual production you should not use ngrok.

Steps to use ngrok:
1. Open powershell or your terminal
2. Naviage to the directory where you downloaded ngrok
3. Run ngrok by typing ./ngrok http 5000

Now, if sucessful ngrok should be running on port 5000. So anything running on
5000 with be accessible using the ngrok URL



