# The Grail

## Website made with Django focused on the mobile game Fate/Grand Order.

The site uses the [Atlas Academy API](https://api.atlasacademy.io) to retrieve datamined and up to date values for the different parameters of the playable characters in the game (servants) as well as other relevant information in order to analyse different configurations and strategies.

For now the service only calculates damage in simple scenarios but the idea is to extend this to enemies and nodes from future events in order to optimise resource management in things such as Fou cards, NP levels or grails. To do so, we use the fact that there is a 2 year delay between the events in the JP version with respect to the NA version as well as the information available about this on wikia by using the MediaWiki API through <code>pywikibot</code>.
