import sys
import tweepy
import config
from googlevoice import Voice

# Declare some globals:
# Keep track of whether twaffic is on or off
toggle_state = 'off'
# Account to listen to for toggle commands
toggle_account = 'ARTestAccount'
# User IDs to follow (toggle account and @MassDOT)
follow_userids = [523460971,23595586]
# Traffic alert filter text so we only get @MassDOT's traffic statuses
filter = 'Traffic'


# Define a subclass of tweepy's StreamListener to create a custom listener
class Listener(tweepy.StreamListener):

    def on_status(self, status):
        # Grab global toggle state
        global toggle_state


        try:
            # Listen for commands and change twaffic state accordingly. Send an SMS when status has been toggled.
            if (status.author.screen_name == toggle_account) and (status.text.find('twafficon') != -1):
                toggle_state = 'on'
                voice.send_sms(config.sms_phone_number, 'twaffic is on')
                
            elif (status.author.screen_name == toggle_account) and (status.text.find('twafficoff') != -1):
                toggle_state = 'off'
                voice.send_sms(config.sms_phone_number, 'twaffic is off')
                
            # If we're on and we get a traffic alert, send a text and record print the full status info to STDOUT
            if toggle_state == 'on':
                if status.text.find(filter) != -1:
                    voice.send_sms(config.sms_phone_number, status.text)
                    print "Sending: %s\t%s\t%s\t%s" % (status.text, 
                                                       status.author.screen_name, 
                                                       status.created_at, 
                                                       status.source,)

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


# Configure and run the twaffic stream listener:
# configure GVoice account
voice = Voice()
voice.login(email=config.gvoice_email, passwd=config.gvoice_pass)

# configure twitter client
auth = tweepy.OAuthHandler(config.tw_consumer_key, config.tw_consumer_secret)
auth.set_access_token(config.tw_token, config.tw_token_secret)
twitter = tweepy.API(auth)

# Here's the business end:
try:
    streamer = tweepy.streaming.Stream(auth, Listener(), timeout=60)
    streamer.filter(follow=follow_userids)

except KeyboardInterrupt:
    print "\nGoodbye..."
    exit
