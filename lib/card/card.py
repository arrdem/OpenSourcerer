#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   card.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

from ..client import Client
from ..db.card_parser import *
import re

class Card(Client):

    __handlers__   = None
    __status__     = 0     # 0: deck, 1: hand, -1: Gyard, -2: exile
    __fields__     = ['name', 'cost', 'types', 'text', 'flavor_text',
                      'keywords', 'power', 'toughness', 'rarity', 'expansion',
                      'abilities', 'effects', 'muid', 'use_count',
                      'deck_count', 'loyalty', 'rating', 'img', 'meta']

    __keywords__   = ["Absorb", "Affinity", "Amplify", "Annihilator", "Attach",
                      "Aura swap", "Banding", "Bands with other",
                      "Bloodthirst", "Bury", "Bushido", "Buyback", "Cascade",
                      "Champion", "Changeling", "Channel", "Chroma", "Clash",
                      "Conspire", "Convoke", "Counter", "Cumulative Upkeep",
                      "Cycling", "Deathtouch", "Defender", "Delve", "Devour",
                      "Domain", "Double strike", "Dredge", "Echo", "Enchant",
                      "Entwine", "Epic", "Equip", "Evoke", "Exalted", "Exile",
                      "Fading", "Fateseal", "Fear", "First strike", "Flanking",
                      "Flash", "Flashback", "Flying", "Forecast", "Fortify",
                      "Frenzy", "Graft", "Grandeur", "Gravestorm", "Haste",
                      "Haunt", "Hellbent", "Hexproof", "Hideaway",
                      "Horsemanship", "Imprint", "Infect", "Intimidate",
                      "Join forces", "Kicker", "Kinship", "Landfall",
                      "Swampwalk", "Islandwalk", "Mountainwalk", "Forestwalk",
                      "Planeswalk", "Landwalk", "Swamphome", "Islandhome",
                      "Mountainhome", "Foresthome", "Planeshome", "Landhome",
                      "Level up", "Lifelink", "Madness", "Metalcraft",
                      "Modular", "Morph", "Multikicker", "Ninjuts", "Offering",
                      "Persist", "Phasing", "Poisonous", "Protection",
                      "Provoke", "Prowl", "Radiance", "Rampage", "Reach",
                      "Rebound", "Recover", "Regenerate", "Reinforce",
                      "Replicate", "Retrace", "Ripple", "Sacrifice", "Scry",
                      "Shadow", "Shroud", "Soulshift", "Splice",
                      "Split second", "Storm", "Substance", "Sunburst",
                      "Suspend", "Sweep", "Tap", "Threshold", "Kicker",
                      "Trample", "Transfigure", "Transmute", "Totem armor",
                      "Unearth", "Untap", "Vanishing", "Vigilance", "Wither"]

    __gatherer_html_ids__ = \
    ['ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_totalVotes',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage',
     ]

    """
    This object serves to represent a basic card/spell as it would be in
    a deck or hand. Because I already have the old mcardlib from the
    first downloader I'm going to do something stupid and dangerous here
    to initialize my class member variables:
        I am going to take a dict of card data in the constructor
        and I am going to UPDATE self.__dict__ LIKE A MOFO BAUS
    """

    def __init__(self, gi, d):
        Client.__init__(self, gi)
        self.__dict__.update(d)
        self.__handlers__ = {}
        self.__record__   = {}

    def __handle__(self, sig):
        if(sig.__class__ in self.__handlers__):
            f = self.__handlers__[sig]
            f(self, sig)

    def __null__(self, sig):
        return

    def __add_handler_method__(self, sig, handler):
        self.__hanlers__[sig.__class__] = setattr(self,
                                             func.__name__,
                                             types.MethodType(handler, self))

    def __getitem__(self, key):
        if key in self.__record__:
            return self.__record__[key]
        else:
            return None

    def __setitem__(self, key, value):
        self.__record__[key] = value

    def loadFromTCGPlayer(self, html):
        pass

    def loadFromGatherer(self, html):
        p = WebPage()
        p.feed(html)
        tree = p.__tree_root__

        # limit the syntax tree to the subtree making up the right column
        limited_tree = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rightCol'))

        # first get the easy stuff...
        ## get the card's name
        res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow'))
        res = next(res.find(lambda x: x['class'] == 'value'))
        self.name = res['data'].strip()

        ## get the card's flavor text
        try:
            res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorText'))
            self.flavor_text = res.join(recursive=True).strip()
        except StopIteration:
            self.flavor_text = "None"

        ## get the card's core text
        try:
            res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow'))
            res = res.__children__[1]
            self.text = ""
            for c in res.__children__:
                self.text += (c.__fields__['data'] + '\n')
        except StopIteration:
            self.text = "None"


        ## get the card's types
        res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow'))
        res = next(res.find(lambda x: x['class'] == 'value'))
        self.types = [s.strip() for s in res['data'].strip().split('-')]

        # now for the stuff which needs a little processing...
        ## get the power and toughness
        try:
            res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow'))
            res = next(res.find(lambda x: x['class'] == 'value'))
            self.power, self.toughness = (int(s) for s in res['data'].strip().split('\\'))
        except StopIteration:
            self.power, self.toughness = -1,-1

        ## get the explicit mana cost
        res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow'))
        res = next(res.find(lambda x: x['class'] == 'value'))

        self.cost = {'Black': 0, 'White': 0, 'Blue': 0, 'Green': 0, 'Red': 0,
                     'Phyrexian': 0, 'X': False}

        for child in res.__children__:
            try:
                i = int(child.__fields__['alt'])
                self.cost['*'] = i
            except:
                s = child.__fields__['alt']
                if "Phyrexian" in s:
                    s = s.split(' ')[1]
                    self.cost['Phyrexian'] += 1

                elif 'Variable Colorless' == s:
                    self.cost['X'] = True
                    continue

                self.cost[s] += 1

        ## get the converted cost row
        res = next(limited_tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow'))
        res = next(res.find(lambda x: x['class'] == 'value'))
        self.ccost = int(res.__fields__['data'].strip('"').strip())

        ## get the expansion
        res = next(limited_tree.find(lambda x:'id' in x and x['id'] == "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"))
        res = res.__children__[1]
        self.expansion = res.__fields__['data']

        ## get the rarity
        res = next(limited_tree.find(lambda x:'id' in x and x['id'] == "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"))
        res = res.__children__[1]
        self.rarity = res.__str__().strip()

        ## get the rating
        self.rating = float(
                       next(
                        limited_tree.find(
                         lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRating'))['data'])

        ## get the MUID
        res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage'))
        m = re.findall('multiverseid=([0-9]+)', res.__fields__['src'])
        self.muid = int(m[0])

        ## get the image URL
        ### a constant string and the MUID
        self.img = ("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%i&type=card" % self.muid)

        self.keywords = [ k for k in self.__keywords__ if k.lower() in self.text.lower()]

if __name__ == "__main__" or 1:

    c = Card(None, [])
    c.loadFromGatherer("""
<html>
<body>
<div>

	<input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="" />
	<input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="" />
	<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="/wEWBgKBx/f1CgKw+7DyCgKKqPSlCQLIiJiWCgLgiMDeAwKBjNExzlwNG+VjazOiCGcrd1YqUcDjdvo=" />
</div>
    <div style="width: 100%; height: 1px;">
    </div>
    <div id="ctl00_ctl00_ctl00_MainContainer" class="mainContainer">
        <div class="leftContainer">
            <div id="ctl00_ctl00_ctl00_TopBannerAdvertisementCMS" class="topBanner"><body docname="mtg_gatherer_banner_advertisement" doclang="en" xmlPath="" useDate="3/12/2012">
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

    <span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay">Act of Aggression</span>

                </div>

    <ul id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_ContentNavigationControlsContainer" class="contentlinks">
    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Discussion"><a href="Discussion.aspx?multiverseid=230076" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_DiscussionLink"><span>Discussion</span></a></li>

    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Languages"><a href="Languages.aspx?multiverseid=230076" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_LanguagesLink"><span>Languages</span></a></li>
    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Printings"><a href="Printings.aspx?multiverseid=230076" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_PrintingsLink"><span>Sets &amp; Legality</span></a></li>
    <li id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_Details" class="current"><a href="Details.aspx?multiverseid=230076" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_DetailsLink"><span>Details</span></a></li>
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
                <img src="../../Handlers/Image.ashx?multiverseid=230076&amp;type=card" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage" alt="Act of Aggression" style="border:none;" />

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
                        Display: <b><a id="cardTextSwitchLink1" href='/Pages/Card/Details.aspx?printed=false&multiverseid=230076' class="selected">Oracle</a></b> | <a id="cardTextSwitchLink2" href='/Pages/Card/Details.aspx?printed=true&multiverseid=230076'>Printed</a>

                    </div>
                    <b class="ff"><b></b></b>
                </div>
                <div class="smallGreyMono" style="margin-top: 10px;">
                    <b class="ft"><b></b></b>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow" class="row">
                        <div class="label">
                            Card Name:</div>
                        <div class="value">
                            Act of Aggression</div>
                    </div>

                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow" class="row">
                        <div class="label" style="line-height:25px;">
                            Mana Cost:</div>
                        <div class="value">
                            <img src="/Handlers/Image.ashx?size=medium&amp;name=3&amp;type=symbol" alt="3" align="absbottom" /><img src="/Handlers/Image.ashx?size=medium&amp;name=RP&amp;type=symbol" alt="Phyrexian Red" align="absbottom" /><img src="/Handlers/Image.ashx?size=medium&amp;name=RP&amp;type=symbol" alt="Phyrexian Red" align="absbottom" /></div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow" class="row" style="height:15px; position:relative;">
                        <div class="label" style="font-size:.7em;">
                            Converted Mana Cost:</div>
                        <div class="value">
                            5<br /><br /></div>
                    </div>

                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow" class="row">
                        <div class="label">
                            Types:</div>
                        <div class="value">
                            Instant</div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow" class="row">
                        <div class="label">
                            Card Text:</div>
                        <div class="value">
                            <div class="cardtextbox"><i>(<img src="/Handlers/Image.ashx?size=small&amp;name=RP&amp;type=symbol" alt="Phyrexian Red" align="absbottom" /> can be paid with either <img src="/Handlers/Image.ashx?size=small&amp;name=R&amp;type=symbol" alt="Red" align="absbottom" /> or 2 life.)</i></div><div class="cardtextbox">Gain control of target creature an opponent controls until end of turn. Untap that creature. It gains haste until end of turn.</div></div>
                    </div>

                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_markRow" class="row">
                        <div class="label">
                            Watermark:</div>
                        <div class="value">
                            <div class="cardtextbox"><i>Phyrexian</i></div></div>
                    </div>


                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow" class="row">
                        <div class="label">
                            Expansion:</div>
                        <div class="value">
                            <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol">
	<a href="Details.aspx?multiverseid=230076"><img title="New Phyrexia (Uncommon)" src="../../Handlers/Image.ashx?type=symbol&amp;set=NPH&amp;size=small&amp;rarity=U" alt="New Phyrexia (Uncommon)" align="absmiddle" style="border-width:0px;" /></a>
                                <a href="/Pages/Search/Default.aspx?action=advanced&amp;set=[%22New Phyrexia%22]">New Phyrexia</a>

</div>
                        </div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow" class="row">
                        <div class="label">
                            Rarity:</div>
                        <div class="value">
                            <span class='uncommon'>Uncommon</span></div>
                    </div>

                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow" class="row">
                        <div class="label">
                            Card #:</div>
                        <div class="value">
                            78</div>
                    </div>
                    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow" class="row">
                        <div class="label">
                            Artist:</div>
                        <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit" class="value">
                            <a href="/Pages/Search/Default.aspx?action=advanced&amp;artist=[%22Whit Brachna%22]">Whit Brachna</a></div>
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
                            <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_starRating" class="starRating"><img src="../../Images/Stars/LeftSolid.gif" alt="0.5" /><img src="../../Images/Stars/RightSolid.gif" alt="1.0" /><img src="../../Images/Stars/LeftSolid.gif" alt="1.5" /><img src="../../Images/Stars/RightSolid.gif" alt="2.0" /><img src="../../Images/Stars/LeftSolid.gif" alt="2.5" /><img src="../../Images/Stars/RightSolid.gif" alt="3.0" /><img src="../../Images/Stars/LeftSolid.gif" alt="3.5" /><img src="../../Images/Stars/RightClear.gif" alt="4.0" /><img src="../../Images/Stars/LeftClear.gif" alt="4.5" /><img src="../../Images/Stars/RightClear.gif" alt="5.0" />
    <br/>
    <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRatingContainer" class="textRating">
        Rating: <span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRating" class="textRatingValue">3.747</span> / 5&nbsp;&nbsp;(<span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_totalVotes" class="totalVotesValue">75</span><span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_extraVoteInfo"> votes</span>)</div>
</div>

                        </div>
                    </div>
                    <div style="padding-left: 5px; font-size:.85em;">
                        Click <a href="/Pages/Card/Discussion.aspx?multiverseid=230076" id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_discussionLink">here</a> to <b>rate</b> and
                        <b>discuss</b> this card.</div>
                    <b class="ff"><b></b></b>
                </div>
            </td>

        </tr>
        <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRow">
	<td colspan="2">
                <div class="smallGreyBorder">
                    <b class="at"><b></b></b>
                    <div class="simpleRoundedBoxTitleGrey">
                        <span class="boldtitle">Rulings</span></div>
                    <div class="discussion">
                        <a href="javascript:void(0);" onclick="SaveVisibleArea(event, this, ClientIDs.rulingsContainer, 'rulingsContainer', false); return DisplayRulings(event, this, 'Display Rulings', 'Hide Rulings');"
                            class="collapsedNode"><b>
                                Display Rulings</b></a>
                        <div id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsContainer" class="postContainer" style="display:none;">
                            <table cellpadding="0" cellspacing="0">

                                        <tr class="post evenItem" style="background-color: #efefef;">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl00_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl00_rulingText" style="width: 610px; padding-right: 5px;">A card with Phyrexian mana symbols in its mana cost is each color that appears in that mana cost, regardless of how that cost may have been paid.</td>

                                        </tr>

                                        <tr class="post oddItem">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl01_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl01_rulingText" style="width: 610px; padding-right: 5px;">To calculate the converted mana cost of a card with Phyrexian mana symbols in its cost, count each Phyrexian mana symbol as 1.</td>

                                        </tr>

                                        <tr class="post evenItem" style="background-color: #efefef;">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl02_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl02_rulingText" style="width: 610px; padding-right: 5px;">As you cast a spell or activate an activated ability with one or more Phyrexian mana symbols in its cost, you choose how to pay for each Phyrexian mana symbol at the same time you would choose modes or choose a value for X.</td>

                                        </tr>

                                        <tr class="post oddItem">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl03_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl03_rulingText" style="width: 610px; padding-right: 5px;">If you're at 1 life or less, you can't pay 2 life.</td>

                                        </tr>

                                        <tr class="post evenItem" style="background-color: #efefef;">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl04_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl04_rulingText" style="width: 610px; padding-right: 5px;">Phyrexian mana is not a new color. Players can't add Phyrexian mana to their mana pools.</td>

                                        </tr>

                                        <tr class="post oddItem">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl05_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl05_rulingText" style="width: 610px; padding-right: 5px;">Act of Aggression can target any creature an opponent controls, even one that's untapped.</td>

                                        </tr>

                                        <tr class="post evenItem" style="background-color: #efefef;">
                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl06_rulingDate" style="width: 70px; padding-left: 10px; font-weight: bold;">6/1/2011</td>

                                            <td id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rulingsRepeater_ctl06_rulingText" style="width: 610px; padding-right: 5px;">Gaining control of a creature doesn't cause you to gain control of any Auras or Equipment attached to it.</td>

                                        </tr>

                            </table>
                        </div>
                    </div>
                    <b class="aa"><b></b></b>
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
                    <a href="../Login.aspx?returnurl=%2fPages%2fCard%2fDetails.aspx%3fmultiverseid%3d230076">Login</a>
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
</form>
</body>
</html>
""")
    for k in c.__fields__:
        print(k, getattr(c, k))
