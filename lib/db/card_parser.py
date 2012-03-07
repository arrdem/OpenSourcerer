#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from html.parser import HTMLParser

class HTMLTree():
    __id_counter__ = 1
    def __init__(self, *args, **kwargs):
        self.__children__   = []
        self.__fields__     = {'data':'', '_tree_id':int(self.__id_counter__)}
        self.__parent__     = None
        self.__id_counter__ += 1

    def __getitem__(self, key):
        if key in self.__fields__:
            return self.__fields__[key]
        else:
            return None

    def __setitem__(self, key, value):
        self.__fields__[key] = value

    def __str__(self, long = 0):
        if(long == 0):
            return self.__fields__['_type']
        elif(long == 1):
            return str(self.__fields__)
        elif(long > 1):
            self.__fields__['_type'] + "\n".join([str(a) for a in self.__children__])

    def search(self, f):
        """
        All I'm going to say about this method is that while it does a
        revolting O(n) search of the graph (has to, no order) it can
        take any number of really cute lambda functions for f ;-)
        """
        l = self.__children__ + ([self] if self.__parent__ == None else [])
        for node in l:
            if(f(node.__fields__)):
                yield node

        for c in self.__children__:
            for n in c.search(f):
                yield n

class WebPage(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        # set up locals..
        self.__tree_root__ = HTMLTree()
        self.__cursor__ = self.__tree_root__

    def handle_starttag(self, tag, attrs):
        t = HTMLTree()
        self.__cursor__.__children__.append(t)
        t.__parent__ = self.__cursor__
        self.__cursor__ = t
        self.__cursor__['_type'] = tag
        self.__cursor__.__fields__.update(dict(attrs))

    def handle_endtag(self, tag):
        if self.__cursor__.__parent__:
            self.__cursor__ = self.__cursor__.__parent__

    def handle_data(self, data):
        self.__cursor__['data'] += data

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass

if __name__ == "__main__":
    parser = WebPage()
    parser.feed("""

<?xml version="1.0" encoding="utf-8" ?>



<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>
    Shivan Dragon (Masters Edition IV) - Gatherer - Magic: The Gathering
</title><link rel="shortcut icon" href="/Images/favicon.ico" /><meta name="description" content="Gatherer is the Magic Card Database. Search for the perfect addition to your deck. Browse through cards from Magic's entire history. See cards from the most recent sets and discover what players just like you are saying about them." /><meta name="keywords" content="monitor, gatherer, magic cards, magic the gathering, black lotus, magic: the gathering, wizards of the coast, wizards, trading card game, trading cards, collectible card game, tcg, ccg, magic sets, game, multiplayer, hobby" />

    <!-- google analytics -->
    <script type="text/javascript">
    var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
    document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
    try {
    var pageTracker = _gat._getTracker("UA-15020098-7");
    pageTracker._setDomainName(".wizards.com");
    pageTracker._trackPageview();
    } catch(err) {}
    </script>
<link type="text/css" rel="stylesheet" media="screen" href="../../Styles/Styles.css" /><link href="/WebResource.axd?d=GRnNg3t4K46DgrIFhLf_9NAuUGNb9hPC5E3VRvvs03EEanuwjppIYb1ygZbulkgS4u5w9pKS9Yy4Yj6i6DYt9MPjPepf71AnWzo4xZTSDC41&amp;amp;t=634661344835867613" rel="icon" type="image/ico" /></head>
<body>


    <form method="post" action="Details.aspx?multiverseid=228264" id="aspnetForm">
<div>
<input type="hidden" name="__LASTFOCUS" id="__LASTFOCUS" value="" />
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUKLTQxOTY5NzI3NGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgMFO2N0bDAwJGN0bDAwJGN0bDAwJE1haW5Db250ZW50JFNlYXJjaENvbnRyb2xzJFNlYXJjaENhcmROYW1lBTxjdGwwMCRjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTZWFyY2hDb250cm9scyRTZWFyY2hDYXJkVHlwZXMFO2N0bDAwJGN0bDAwJGN0bDAwJE1haW5Db250ZW50JFNlYXJjaENvbnRyb2xzJFNlYXJjaENhcmRUZXh08eaAgh/v97psiSof7KwBwiyoYMg=" />
</div>

<script type="text/javascript">
//<![CDATA[
var theForm = document.forms['aspnetForm'];
if (!theForm) {
    theForm = document.aspnetForm;
}
function __doPostBack(eventTarget, eventArgument) {
    if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
        theForm.__EVENTTARGET.value = eventTarget;
        theForm.__EVENTARGUMENT.value = eventArgument;
        theForm.submit();
    }
}
//]]>
</script>


<script src="/WebResource.axd?d=RfPwrpEpsgfK5qe9MY0Brg2&amp;t=633608243254431488" type="text/javascript"></script>


<script src="../../Scripts/Prototype.js" type="text/javascript"></script>
<script src="../../Scripts/Utilities.js" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[
var cardSearchPage = '/Pages/Search/Default.aspx';
var leftStar = '../../Images/Stars/LeftSolid.gif';
var leftStarClear = '../../Images/Stars/LeftClear.gif';
var leftStarSelected = '../../Images/Stars/LeftSelected.gif';
var rightStar = '../../Images/Stars/RightSolid.gif';
var rightStarClear = '../../Images/Stars/RightClear.gif';
var rightStarSelected = '../../Images/Stars/RightSelected.gif';
var utilitiesHandler = '../../Handlers/RPCUtilities.ashx';
var CardDatabaseSettings = 'CardDatabaseSettings';
var SelectingCardAction = 'NavigatesToCard';
var inlineCardSearchHandler = '/Handlers/InlineCardSearch.ashx';
var autoCompleteGroupBy = 'None';
var imageHandler = '/Handlers/Image.ashx';
var cardDetailsPage = '/Pages/Card/Details.aspx';
var UtilitiesHandler = '/Handlers/RPCUtilities.ashx';

var enableCardSearchAutoComplete = true;
var enableHintText = true;
var enableCardSearchAutoCompleteIfNameUnchecked = false;



function ClientIDs() {}
ClientIDs.MainForm = 'aspnetForm';
ClientIDs.MainContainer = 'ctl00_ctl00_ctl00_MainContainer';
ClientIDs.TopBannerAdvertisementCMS = 'ctl00_ctl00_ctl00_TopBannerAdvertisementCMS';
ClientIDs.gathererIntroText = 'ctl00_ctl00_ctl00_gathererIntroText';
ClientIDs.gathererWelcome = 'ctl00_ctl00_ctl00_gathererWelcome';
ClientIDs.MainContent = 'ctl00_ctl00_ctl00_MainContent';
ClientIDs.NavigationLinks = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks';
ClientIDs.NavigationAnchorsContainer = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_NavigationAnchorsContainer';
ClientIDs.Simple = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Simple';
ClientIDs.Advanced = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Advanced';
ClientIDs.Random = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Random';
ClientIDs.Settings = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Settings';
ClientIDs.Language = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Language';
ClientIDs.Help = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Help';
ClientIDs.Configuration = 'ctl00_ctl00_ctl00_MainContent_NavigationLinks_Configuration';
ClientIDs.SearchControls = 'ctl00_ctl00_ctl00_MainContent_SearchControls';
ClientIDs.SearchBoxContainer = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxContainer';
ClientIDs.CardSearchBoxParent = 'ctl00_ctl00_ctl00_MainContent_SearchControls_CardSearchBoxParent';
ClientIDs.CardSearchBox = 'ctl00_ctl00_ctl00_MainContent_SearchControls_CardSearchBoxParent_CardSearchBox';
ClientIDs.searchSubmitButton = 'ctl00_ctl00_ctl00_MainContent_SearchControls_searchSubmitButton';
ClientIDs.SearchBoxResults = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxResults';
ClientIDs.SearchBoxResultsTitle = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxResultsTitle';
ClientIDs.SearchBoxResultsContent = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxResultsContent';
ClientIDs.AllResultsLink = 'ctl00_ctl00_ctl00_MainContent_SearchControls_AllResultsLink';
ClientIDs.SearchSettings = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchSettings';
ClientIDs.searchControlsContainer = 'ctl00_ctl00_ctl00_MainContent_SearchControls_searchControlsContainer';
ClientIDs.SearchCardName = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchCardName';
ClientIDs.SearchCardTypes = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchCardTypes';
ClientIDs.SearchCardText = 'ctl00_ctl00_ctl00_MainContent_SearchControls_SearchCardText';
ClientIDs.SubContent = 'ctl00_ctl00_ctl00_MainContent_SubContent';
ClientIDs.SubContentHeader = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader';
ClientIDs.subtitleDisplay = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay';
ClientIDs.SubContentAnchors = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors';
ClientIDs.DetailsAnchors = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors';
ClientIDs.ContentNavigationControlsContainer = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_ContentNavigationControlsContainer';
ClientIDs.Discussion = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Discussion';
ClientIDs.DiscussionLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_DiscussionLink';
ClientIDs.Artwork = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Artwork';
ClientIDs.ArtworkLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_ArtworkLink';
ClientIDs.Languages = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Languages';
ClientIDs.LanguagesLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_LanguagesLink';
ClientIDs.Printings = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Printings';
ClientIDs.PrintingsLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_PrintingsLink';
ClientIDs.Details = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Details';
ClientIDs.DetailsLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_DetailsLink';
ClientIDs.topPagingControlsContainer = 'ctl00_ctl00_ctl00_MainContent_SubContent_topPagingControlsContainer';
ClientIDs.cardAdminControls = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardAdminControls';
ClientIDs.editLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_editLink';
ClientIDs.imageDivContainer = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_imageDivContainer';
ClientIDs.image = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_image';
ClientIDs.otherVariationsOverlay = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherVariationsOverlay';
ClientIDs.otherVariationsOverlation = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherVariationsOverlation';
ClientIDs.overlayVariationLinks = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_overlayVariationLinks';
ClientIDs.wordingWrapperRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_wordingWrapperRow';
ClientIDs.wordingWrapper = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_wordingWrapper';
ClientIDs.cardComponent0 = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardComponent0';
ClientIDs.imagePlaceHolder = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_imagePlaceHolder';
ClientIDs.cardImage = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage';
ClientIDs.specialCaseBreaker = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_specialCaseBreaker';
ClientIDs.otherVariations = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherVariations';
ClientIDs.variationLinks = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_variationLinks';
ClientIDs.specialCaseLayoutBreakers = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_specialCaseLayoutBreakers';
ClientIDs.rightCol = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rightCol';
ClientIDs.cardWordingSwitch = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardWordingSwitch';
ClientIDs.cardParts = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardParts';
ClientIDs.nameRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow';
ClientIDs.nameLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameLabel';
ClientIDs.nameValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameValue';
ClientIDs.manaRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow';
ClientIDs.manacostLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manacostLabel';
ClientIDs.manacostValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manacostValue';
ClientIDs.cmcRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow';
ClientIDs.cmcLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcLabel';
ClientIDs.cmcValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcValue';
ClientIDs.typeRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow';
ClientIDs.typeLineLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeLineLabel';
ClientIDs.typeLineValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeLineValue';
ClientIDs.textRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow';
ClientIDs.cardTextLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardTextLabel';
ClientIDs.cardTextValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardTextValue';
ClientIDs.flavorRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow';
ClientIDs.flavorTextLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorTextLabel';
ClientIDs.FlavorText = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText';
ClientIDs.flavorTextValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorTextValue';
ClientIDs.markRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_markRow';
ClientIDs.markTextLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_markTextLabel';
ClientIDs.markTextValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_markTextValue';
ClientIDs.colorIndicatorRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_colorIndicatorRow';
ClientIDs.colorIndicatorLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_colorIndicatorLabel';
ClientIDs.colorIndicatorValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_colorIndicatorValue';
ClientIDs.ptRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow';
ClientIDs.bottomNumbersLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_bottomNumbersLabel';
ClientIDs.bottomNumbersValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_bottomNumbersValue';
ClientIDs.setRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow';
ClientIDs.setLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setLabel';
ClientIDs.currentSetSymbol = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol';
ClientIDs.setValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setValue';
ClientIDs.rarityRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow';
ClientIDs.rarityLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityLabel';
ClientIDs.rarityValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityValue';
ClientIDs.otherSetsRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsRow';
ClientIDs.otherSetsLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsLabel';
ClientIDs.otherSetsValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue';
ClientIDs.numberRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow';
ClientIDs.numberLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberLabel';
ClientIDs.numberValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberValue';
ClientIDs.artistRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow';
ClientIDs.artistLabel = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistLabel';
ClientIDs.ArtistCredit = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit';
ClientIDs.artistValue = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistValue';
ClientIDs.playerRatingRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow';
ClientIDs.ratingResult = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ratingResult';
ClientIDs.currentRating = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating';
ClientIDs.starRating = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_starRating';
ClientIDs.textRatingContainer = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRatingContainer';
ClientIDs.textRating = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRating';
ClientIDs.totalVotes = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_totalVotes';
ClientIDs.extraVoteInfo = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_extraVoteInfo';
ClientIDs.discussionLink = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_discussionLink';
ClientIDs.rulingsRow = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRow';
ClientIDs.rulingsContainer = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsContainer';
ClientIDs.rulingsRepeater = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater';
ClientIDs.cardComponent1 = 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardComponent1';
ClientIDs.bottomPagingControlsContainer = 'ctl00_ctl00_ctl00_MainContent_SubContent_bottomPagingControlsContainer';
ClientIDs.loginLinkPlaceholder = 'ctl00_ctl00_ctl00_loginLinkPlaceholder';
ClientIDs.CopyrightYear = 'ctl00_ctl00_ctl00_CopyrightYear';
ClientIDs.RightBannerAdvertisement = 'ctl00_ctl00_ctl00_RightBannerAdvertisement';
var textBoxHash = new Hash( { ctl00_ctl00_ctl00_MainContent_SearchControls_CardSearchBoxParent_CardSearchBox: 'Search Terms...' } );//]]>
</script>

<script src="../../Scripts/Constants.js" type="text/javascript"></script>
<script src="../../Scripts/CardDatabase.js" type="text/javascript"></script>
<script src="../../Scripts/CardDetails.js" type="text/javascript"></script>
<script src="../../Scripts/StarRating.js" type="text/javascript"></script>
<script src="../../Scripts/SearchControls.js" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[
Event.observe(window, 'load', SubscribeToStarEvents);
//]]>
</script>

<script src="/WebResource.axd?d=udx9mWLFOFHiLwSc_-Vyog2&amp;t=633608243254431488" type="text/javascript"></script>
    <div style="width: 100%; height: 1px;">
    </div>
    <div id="ctl00_ctl00_ctl00_MainContainer" class="mainContainer">
        <div class="leftContainer">
            <div id="ctl00_ctl00_ctl00_TopBannerAdvertisementCMS" class="topBanner"><body docname="mtg_gatherer_banner_advertisement" doclang="en" xmlPath="" useDate="3/6/2012">
  <a target="_blank" href="http://www.wizards.com/magic/tcg/productarticle.aspx?x=mtg/tcg/magicthegatheringtoolbox/productinfo">
    <img src="http://media.wizards.com/images/magic/daily/ads/20120207_mtgtoolbox_728.jpg" />
  </a>
</body></div>
            <div class="background">
                <div class="top">
                    <div class="left">
                    </div>
                    <div class="middle">
                    </div>
                    <div class="right">
                    </div>
                </div>
                <div class="center">
                    <div class="middle">
                        <div class="middleright">
                            <div class="gathererContent">


<div class="logo">
    <a class="magic" href="http://www.magicthegathering.com"></a>
    <a href="../Default.aspx" class="cardDatabase"></a>
</div>



    <div id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_NavigationAnchorsContainer" class="searchcontrollinks">
    <a href="../Default.aspx" id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_Simple" class="current">Simple</a>
    <a href="../Advanced.aspx" id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_Advanced">Advanced</a>
    <a href="Details.aspx?action=random" id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_Random">Random Card</a>
    <a href="../Settings.aspx" id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_Settings">Settings</a>
    <a href="../Language.aspx" id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_Language">Language</a>
    <a href="../Help.aspx" id="ctl00_ctl00_ctl00_MainContent_NavigationLinks_Help">Help</a>

</div>



<div class="searchcontrols">
    <div id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxContainer" class="searchboxcontainertop">


<div class="textbox" id="ctl00_ctl00_ctl00_MainContent_SearchControls_CardSearchBoxParent" style=""><input name="ctl00$ctl00$ctl00$MainContent$SearchControls$CardSearchBoxParent$CardSearchBox" type="text" id="ctl00_ctl00_ctl00_MainContent_SearchControls_CardSearchBoxParent_CardSearchBox" class="textboxinput" onblur="SetCurrentControlBlur(event)" onfocus="SetCurrentControlFocus(event, this);" autocomplete="off" maxlength="50" /></div>
    </div>
    <div class="searchsubmit">
        <input type="submit" name="ctl00$ctl00$ctl00$MainContent$SearchControls$searchSubmitButton" value="Search" id="ctl00_ctl00_ctl00_MainContent_SearchControls_searchSubmitButton" class="searchbutton" />
    </div>
    <br class="clear" />
    <!-- Autocomplete Results -->
    <div id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxResults" class="searchresultscontainertop">
        <div class="smallGreyBorder">
            <b class="ct"><b></b></b>
            <div class="simpleRoundedBoxTitleGrey">
                <span id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxResultsTitle" class="boldtitle">Results </span>
            </div>
            <div id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchBoxResultsContent" style="background-color: #b7b7b7;">
            </div>
            <div class="simpleRoundedBoxFooterGrey">
                <span><a href="javascript:void(0);" id="ctl00_ctl00_ctl00_MainContent_SearchControls_AllResultsLink" class="autoCompleteAllResults">
                    All Results</a></span></div>
            <b class="cc"><b></b></b>
        </div>
    </div>
    <!-- /Autocomplete Results -->
    <!-- Search Settings -->
    <div id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchSettings" class="searchsettingsdisplaytop">
        <div class="searchsettings">
            <a href="javascript:void(0);" onclick="SaveVisibleArea(event, this, ClientIDs.searchControlsContainer, 'searchControlsContainer', false); return ToggleSearchSettings(event, this);"
                class="expandedNode"><b>using...</b></a>
            <div id="ctl00_ctl00_ctl00_MainContent_SearchControls_searchControlsContainer">
            <ul>
                <li>
                    <input name="ctl00$ctl00$ctl00$MainContent$SearchControls$SearchCardName" type="checkbox" id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchCardName" checked="checked" onclick="UpdateSimpleSearchFields" />
                    Name</li>
                <li>
                    <input name="ctl00$ctl00$ctl00$MainContent$SearchControls$SearchCardTypes" type="checkbox" id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchCardTypes" onclick="UpdateSimpleSearchFields" />
                    Types</li>
                <li>
                    <input name="ctl00$ctl00$ctl00$MainContent$SearchControls$SearchCardText" type="checkbox" id="ctl00_ctl00_ctl00_MainContent_SearchControls_SearchCardText" onclick="UpdateSimpleSearchFields" />
                    Text</li>
            </ul>
            </div>
        </div>
    </div>
    <!-- /Search Settings -->
</div>
    <br class="clear" />


    <div class="contentcontainer">
        <div class="smallGreyBorder">
            <b class="dt"><b></b></b>
            <div class="simpleRoundedBoxTitleGreyTall">
                <div class="contentTitle">

    <span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay">Shivan Dragon</span>

                </div>

    <ul id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_ContentNavigationControlsContainer" class="contentlinks">
    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Discussion"><a href="Discussion.aspx?multiverseid=228264" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_DiscussionLink"><span>Discussion</span></a></li>

    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Languages"><a href="Languages.aspx?multiverseid=228264" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_LanguagesLink"><span>Languages</span></a></li>
    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Printings"><a href="Printings.aspx?multiverseid=228264" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_PrintingsLink"><span>Sets &amp; Legality</span></a></li>
    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Details" class="current"><a href="Details.aspx?multiverseid=228264" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_DetailsLink"><span>Details</span></a></li>
</ul>


                <div class="pagingcontrols">
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_topPagingControlsContainer" class="paging">
                    </div>
                </div>
            </div>


    <!-- Rotated Image Container -->
    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_imageDivContainer" class="imageContainer">
        <div class="smallGreyBorderBottom">
            <div class="cardViewContainer">
                <div class="close">
                    <a href="javascript:void(0);" onclick="return CloseCardViewer(event, this);"></a>
                </div>
                <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_image" class="imageHolder">
                </div>

                <div class="rotate">
                    <a href="javascript:void(0);" onclick="return RotateCardImage(event, this, false);">
                    </a>
                </div>
            </div>
            <b class="bb"><b></b></b>
        </div>
    </div>
    <!-- End Rotated Image Container -->
    <!-- Card Details Table -->
    <table>
        <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_wordingWrapperRow" style="display: none;">
    <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_wordingWrapper" colspan="2"></td>
</tr>

        <tr>
            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardComponent0" class="cardComponentContainer">
                <table class="cardDetails" style="position: relative; margin: auto;">
        <tr>
            <td class="leftCol" align="center">
                <img src="../../Handlers/Image.ashx?multiverseid=228264&amp;type=card" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage" alt="Shivan Dragon" style="border:none;" />

                <div class="variations">
                    &nbsp;

                </div>
                <div class="rotate">
                    <a href="javascript:void(0)" rel="lightbox" onclick="return RotateCardImage(event, this, true);">
                    </a>
                </div>
            </td>


            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rightCol" class="rightCol">
                <div class="smallGreyMono">
                    <b class="ft"><b></b></b>
                    <div style="padding-left: 5px; font-size:.85em;">
                        Display: <b><a id="cardTextSwitchLink1" href='/Pages/Card/Details.aspx?printed=false&multiverseid=228264' class="selected">Oracle</a></b> | <a id="cardTextSwitchLink2" href='/Pages/Card/Details.aspx?printed=true&multiverseid=228264'>Printed</a>

                    </div>
                    <b class="ff"><b></b></b>
                </div>
                <div class="smallGreyMono" style="margin-top: 10px;">
                    <b class="ft"><b></b></b>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow" class="row">
                        <div class="label">
                            Card Name:</div>
                        <div class="value">
                            Shivan Dragon</div>
                    </div>

                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow" class="row">
                        <div class="label" style="line-height:25px;">
                            Mana Cost:</div>
                        <div class="value">
                            <img src="/Handlers/Image.ashx?size=medium&amp;name=4&amp;type=symbol" alt="4" align="absbottom" /><img src="/Handlers/Image.ashx?size=medium&amp;name=R&amp;type=symbol" alt="Red" align="absbottom" /><img src="/Handlers/Image.ashx?size=medium&amp;name=R&amp;type=symbol" alt="Red" align="absbottom" /></div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow" class="row" style="height:15px; position:relative;">
                        <div class="label" style="font-size:.7em;">
                            Converted Mana Cost:</div>
                        <div class="value">
                            6<br /><br /></div>
                    </div>

                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow" class="row">
                        <div class="label">
                            Types:</div>
                        <div class="value">
                            Creature  — Dragon</div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow" class="row">
                        <div class="label">
                            Card Text:</div>
                        <div class="value">
                            <div class="cardtextbox">Flying</div><div class="cardtextbox"><img src="/Handlers/Image.ashx?size=small&amp;name=R&amp;type=symbol" alt="Red" align="absbottom" />: Shivan Dragon gets +1/+0 until end of turn.</div></div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow" class="row">
                        <div class="label">
                            Flavor Text:</div>
                        <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText" class="value">
                            <div class="cardtextbox"><i>While it's true most Dragons are cruel, the Shivan Dragon seems to take particular glee in the misery of others, often tormenting its victims much like a cat plays with a mouse before delivering the final blow.</i></div></div>
                    </div>


                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow" class="row">
                        <div class="label">
                            P/T:</div>
                        <div class="value">
                            5 / 5</div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow" class="row">
                        <div class="label">
                            Expansion:</div>
                        <div class="value">
                            <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol">
    <a href="Details.aspx?multiverseid=228264"><img title="Masters Edition IV (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=ME4&amp;size=small&amp;rarity=R" alt="Masters Edition IV (Rare)" align="absmiddle" style="border-width:0px;" /></a>
                                <a href="/Pages/Search/Default.aspx?action=advanced&amp;set=[%22Masters Edition IV%22]">Masters Edition IV</a>

</div>
                        </div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow" class="row">
                        <div class="label">
                            Rarity:</div>
                        <div class="value">
                            <span class='rare'>Rare</span></div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsRow" class="row">
                        <div class="label">
                            All Sets:</div>
                        <div class="value">
                            <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue">

                            <a href="Details.aspx?multiverseid=222"><img title="Limited Edition Alpha (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=1E&amp;size=small&amp;rarity=R" alt="Limited Edition Alpha (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=517"><img title="Limited Edition Beta (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=2E&amp;size=small&amp;rarity=R" alt="Limited Edition Beta (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=819"><img title="Unlimited Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=2U&amp;size=small&amp;rarity=R" alt="Unlimited Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=1318"><img title="Revised Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=3E&amp;size=small&amp;rarity=R" alt="Revised Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=2303"><img title="Fourth Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=4E&amp;size=small&amp;rarity=R" alt="Fourth Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=4088"><img title="Fifth Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=5E&amp;size=small&amp;rarity=R" alt="Fifth Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=25688"><img title="Seventh Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=7E&amp;size=small&amp;rarity=R" alt="Seventh Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=45388"><img title="Eighth Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=8ED&amp;size=small&amp;rarity=R" alt="Eighth Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=83259"><img title="Ninth Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=9ED&amp;size=small&amp;rarity=R" alt="Ninth Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=129730"><img title="Tenth Edition (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=10E&amp;size=small&amp;rarity=R" alt="Tenth Edition (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=191320"><img title="Magic 2010 (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=M10&amp;size=small&amp;rarity=R" alt="Magic 2010 (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=26622"><img title="Beatdown Box Set (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=BD&amp;size=small&amp;rarity=R" alt="Beatdown Box Set (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=178025"><img title="From the Vault: Dragons (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=DRB&amp;size=small&amp;rarity=R" alt="From the Vault: Dragons (Rare)" align="absmiddle" style="border-width:0px;" /></a><a href="Details.aspx?multiverseid=228264"><img title="Masters Edition IV (Rare)" src="../../Handlers/Image.ashx?type=symbol&amp;set=ME4&amp;size=small&amp;rarity=R" alt="Masters Edition IV (Rare)" align="absmiddle" style="border-width:0px;" /></a>
</div>
                        </div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow" class="row">
                        <div class="label">
                            Card #:</div>
                        <div class="value">
                            136</div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow" class="row">
                        <div class="label">
                            Artist:</div>
                        <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit" class="value">
                            <a href="/Pages/Search/Default.aspx?action=advanced&amp;artist=[%22Melissa A. Benson%22]">Melissa A. Benson</a></div>
                    </div>
                    <b class="ff"><b></b></b>
                </div>
                <div class="smallGreyMono" style="margin-top: 10px;">
                    <b class="ft"><b></b></b>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow" class="row">
                        <div class="label" style="width:127px; line-height:30px;">
                            Community Rating:</div>
                        <div class="value">
                            <span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ratingResult" class="ratingResult" style="float:right; padding-right:100px; padding-top: 5px; position:relative;"></span>
                            <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_starRating" class="starRating"><img src="../../Images/Stars/LeftSolid.gif" alt="0.5" /><img src="../../Images/Stars/RightSolid.gif" alt="1.0" /><img src="../../Images/Stars/LeftSolid.gif" alt="1.5" /><img src="../../Images/Stars/RightSolid.gif" alt="2.0" /><img src="../../Images/Stars/LeftSolid.gif" alt="2.5" /><img src="../../Images/Stars/RightSolid.gif" alt="3.0" /><img src="../../Images/Stars/LeftSolid.gif" alt="3.5" /><img src="../../Images/Stars/RightSolid.gif" alt="4.0" /><img src="../../Images/Stars/LeftClear.gif" alt="4.5" /><img src="../../Images/Stars/RightClear.gif" alt="5.0" />
    <br/>
    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRatingContainer" class="textRating">
        Rating: <span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRating" class="textRatingValue">4.170</span> / 5&nbsp;&nbsp;(<span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_totalVotes" class="totalVotesValue">44</span><span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_extraVoteInfo"> votes</span>)</div>
</div>

                        </div>
                    </div>
                    <div style="padding-left: 5px; font-size:.85em;">
                        Click <a href="/Pages/Card/Discussion.aspx?multiverseid=228264" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_discussionLink">here</a> to <b>rate</b> and
                        <b>discuss</b> this card.</div>
                    <b class="ff"><b></b></b>
                </div>
            </td>

        </tr>

    </table>
            </td>

            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardComponent1" class="cardComponentContainer">
            </td>

      </tr>
    </table>
    <!-- End Card Details Table -->

            <div class="clear"></div>
            <div id="ctl00_ctl00_ctl00_MainContent_SubContent_bottomPagingControlsContainer">
            </div>
            <b class="dd"><b></b></b>
        </div>
    </div>



                            </div>
                        </div>
                    </div>
                    <div class="bottom">
                        <div class="left">
                        </div>
                        <div class="middle">
                        </div>
                        <div class="right">
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">
                <a href="http://www.magicthegathering.com">magicthegathering.com</a>&nbsp;&nbsp;
                <a href="http://www.wizards.com/magic/Digital/MagicOnline.aspx">Magic: The Gathering
                    Online</a>&nbsp;&nbsp; <a href="../Settings.aspx">Settings</a>&nbsp;&nbsp;
                <a href="../Language.aspx">Language</a>&nbsp;&nbsp; <a href="../Help.aspx">Help</a>&nbsp;|&nbsp;
                    <a href="../Login.aspx?returnurl=%2fPages%2fCard%2fDetails.aspx%3fmultiverseid%3d228264">Login</a>
                <div class="wizardsFooterSection">
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &copy; 1995 - 2012 <a href="http://www.wizards.com">Wizards of the Coast</a> LLC,
                    a subsidiary of Hasbro, Inc. All Rights Reserved.
                </div>
                <br />
                <span class="smalldate"></span>
            </div>
        </div>
        <div class="rightContainer">

        </div>
    </div>

<div>

    <input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="" />
    <input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="" />
    <input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="/wEWBgKBx/f1CgKw+7DyCgKKqPSlCQLIiJiWCgLgiMDeAwKBjNExzlwNG+VjazOiCGcrd1YqUcDjdvo=" />
</div>

<script type="text/javascript">
//<![CDATA[
WebForm_AutoFocus('ctl00_ctl00_ctl00_MainContent_SearchControls_CardSearchBoxParent_CardSearchBox');//]]>
</script>
</form>
</body>
</html>""")

    tree = parser.__tree_root__
    g = tree.search(lambda x: 'id' in x and x['id']=="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow")
    for r in g:
        print(r.__str__(long=1))
