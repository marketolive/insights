from app import app
from flask import request, Response, redirect
import os, requests, re

mpi_host = 'https://sj-ee-api.marketo.com'

@app.route('/')
@app.route('/<path:path>')
def _proxy_2(*args, **kwargs):
	req = requests.request(
		method=request.method,
		url=request.url.replace('http:', 'https:'),
		headers={key: value for (key, value) in request.headers if key != 'Host'},
		data=request.get_data(),
		cookies=request.cookies)
	
	if (re.search('/cmo/v1/metadata/getProgramRank.json', req.url)):
		response = Response('{"success":"true","programCount":"960","program":[{"id":"10536","name":"SEO - Google - US","channelId":"575","metrics":[{"name":"Successes","value":"50621"}]},{"id":"18569","name":"EmSp - eMarketer - USA - Jun 2016","channelId":"350","metrics":[{"name":"Successes","value":"16253"}]},{"id":"18572","name":"WS - Economist Path to 2020 - USA - Jun 2016.01 - Invited","channelId":"429","metrics":[{"name":"Successes","value":"16093"}]},{"id":"19821","name":"EmPr - SMB B2B 5 Things Your Subject Lines Are Missing - USA - Aug 2016","channelId":"429","metrics":[{"name":"Successes","value":"8158"}]},{"id":"12624","name":"EmC - Health Check - APAC - Jun 2015","channelId":"428","metrics":[{"name":"Successes","value":"5279"}]},{"id":"18499","name":"PPC - Google - Marketing Analytics - JPN","channelId":"321","metrics":[{"name":"Successes","value":"5025"}]},{"id":"15248","name":"Website - LaunchPoint: HigherLogic","channelId":"266","metrics":[{"name":"Successes","value":"4807"}]},{"id":"17755","name":"EmSp - Social Media Examiner - USA - Apr 2016","channelId":"350","metrics":[{"name":"Successes","value":"4650"}]},{"id":"5454","name":"Email Sponsored - USA - SocialMediopolis Evergreen - 2017","channelId":"350","metrics":[{"name":"Successes","value":"3855"}]},{"id":"11229","name":"EmC - Community Announcement 2 - USA - Apr 2015","channelId":"428","metrics":[{"name":"Successes","value":"3712"}]},{"id":"13156","name":"Social paid - Facebook - VE 2015 - NOAM","channelId":"339","metrics":[{"name":"Successes","value":"3482"}]},{"id":"22274","name":"EmC - SB - Web Personalization and ABM Promo - USA - Nov 2016.Email 4","channelId":"428","metrics":[{"name":"Successes","value":"3461"}]},{"id":"20275","name":"Display Ad - AdRoll Prosp Virtual Event Sept16 - APAC","channelId":"337","metrics":[{"name":"Successes","value":"3339"}]},{"id":"23944","name":"EmSp - Smart Insights NL - EMEA - Mar 2017","channelId":"350","metrics":[{"name":"Successes","value":"3226"}]},{"id":"10537","name":"SEO - Google - UK","channelId":"575","metrics":[{"name":"Successes","value":"3222"}]},{"id":"19120","name":"PPC - Google Enterprise Campaign - DE","channelId":"321","metrics":[{"name":"Successes","value":"3092"}]},{"id":"18486","name":"Social Paid - Facebook - Blog Subscribe - NA","channelId":"339","metrics":[{"name":"Successes","value":"2942"}]},{"id":"17761","name":"EmPr - SMB B2C Technology Target Account Accelerator - USA - Apr 2016","channelId":"429","metrics":[{"name":"Successes","value":"2721"}]},{"id":"21904","name":"EvF - Marketo Clinic 1214 - JPN - Dec 2016.Invite 2","channelId":"429","metrics":[{"name":"Successes","value":"2621"}]},{"id":"21336","name":"JPN Cheat Sheet - Your Marketing Automation Checklist","channelId":"266","metrics":[{"name":"Successes","value":"2481"}]},{"id":"23582","name":"WS - Forrester Marketing in the Engagement Economy - USA - Mar 2017","channelId":"377","metrics":[{"name":"Successes","value":"2461"}]},{"id":"20629","name":"Nur: NOAM - Competitor - B2B MA Non Specific","channelId":"371","metrics":[{"name":"Successes","value":"2426"}]},{"id":"19962","name":"EvF - Avaus Partner ABM - Nor - EMEA - Nov 2016.Invite 1","channelId":"429","metrics":[{"name":"Successes","value":"2283"}]},{"id":"23856","name":"EmSp - Survey Magazine - USA - Apr 2017","channelId":"350","metrics":[{"name":"Successes","value":"2121"}]},{"id":"23617","name":"PPC - Google - Marketo Brands - JPN","channelId":"321","metrics":[{"name":"Successes","value":"2045"}]},{"id":"21323","name":"EvF - Exec Breakfast Sydney - APAC - Nov 2016.Invite 2","channelId":"429","metrics":[{"name":"Successes","value":"2035"}]},{"id":"10541","name":"SEO - Google - ANZ","channelId":"575","metrics":[{"name":"Successes","value":"2026"}]},{"id":"10542","name":"SEO - Bing - US","channelId":"575","metrics":[{"name":"Successes","value":"2006"}]},{"id":"23922","name":"EvL - ENT - SiriusDecisions - EMEA - Oct 2017","channelId":"373","metrics":[{"name":"Successes","value":"1950"}]},{"id":"17369","name":"PPC - Google Marketing Performance Campaign - FR","channelId":"321","metrics":[{"name":"Successes","value":"1914"}]},{"id":"21316","name":"WM - ABM DEMO - APAC - Oct 2016.Invite 2 - Prospects and Customers","channelId":"428","metrics":[{"name":"Successes","value":"1909"}]},{"id":"18164","name":"EmSp - MarketingProfs Hotline (Bonus) - USA - May 2016","channelId":"350","metrics":[{"name":"Successes","value":"1828"}]},{"id":"14789","name":"EmSp - Entrepreneur - USA - Nov 2015","channelId":"350","metrics":[{"name":"Successes","value":"1813"}]},{"id":"22710","name":"EvF - Marketing Automation for B2B - JPN - Feb 2017.Invite 4","channelId":"429","metrics":[{"name":"Successes","value":"1763"}]},{"id":"22973","name":"WM - News Corp Case Study - Hoosh - APAC - Feb 2017.01 - Invite 1","channelId":"429","metrics":[{"name":"Successes","value":"1744"}]},{"id":"17900","name":"EvL - CEB FSI Tech Summit - USA - Apr 2016","channelId":"373","metrics":[{"name":"Successes","value":"1729"}]},{"id":"19209","name":"EvL - Internet Forum Osaka - JPN - Jul 2016.01 - Invited","channelId":"429","metrics":[{"name":"Successes","value":"1725"}]},{"id":"17374","name":"PPC - Google Lead Management Campaign - DE","channelId":"321","metrics":[{"name":"Successes","value":"1697"}]},{"id":"16265","name":"EvF - Partner Meeting0212 - JPN - Feb 2016.Invite 1 - Edit","channelId":"429","metrics":[{"name":"Successes","value":"1692"}]},{"id":"19455","name":"WS - Keep ABM from A Big Mess - USA - Aug 2016.08 - Follow Up for No Shows","channelId":"428","metrics":[{"name":"Successes","value":"1683"}]},{"id":"20368","name":"Social Paid - Facebook - Gartner 2016 MQ for CRM Lead Mgmt - NOAM","channelId":"339","metrics":[{"name":"Successes","value":"1665"}]},{"id":"18558","name":"EmPr - Digital Marketing 101 - EMEA - Jun 2016","channelId":"429","metrics":[{"name":"Successes","value":"1621"}]},{"id":"21273","name":"Nurture - Asset - DG2LN JPN","channelId":"371","metrics":[{"name":"Successes","value":"1582"}]},{"id":"16262","name":"EmPr - SMB B2B - ABM Primer - USA - Jan 2016","channelId":"429","metrics":[{"name":"Successes","value":"1559"}]},{"id":"17632","name":"EvF - Marketo Clinic 0422 - JPN - Apr 2016.Invite 1","channelId":"429","metrics":[{"name":"Successes","value":"1512"}]},{"id":"22529","name":"EmPr - Driving Client Engagement in FSI - USA - Jan 2017","channelId":"429","metrics":[{"name":"Successes","value":"1479"}]},{"id":"20615","name":"EmPr - B2B - Gartner 2016 MQ for CRM Lead Mgmt Resend - USA - Sept 2016","channelId":"429","metrics":[{"name":"Successes","value":"1460"}]},{"id":"23950","name":"EmPr - SMB B2C Man Crates Case Study - USA - Mar 2017","channelId":"429","metrics":[{"name":"Successes","value":"1456"}]},{"id":"22530","name":"EmPr - SMB B2C Why Marketo Scalability - USA - Jan 2017","channelId":"429","metrics":[{"name":"Successes","value":"1452"}]},{"id":"23446","name":"WM - Marketing Automation for B2B 170315 - JPN - Mar 2017.02 - Invite 2","channelId":"429","metrics":[{"name":"Successes","value":"1383"}]},{"id":"19981","name":"EmSp - DMNews - USA - Aug 2016","channelId":"350","metrics":[{"name":"Successes","value":"1346"}]},{"id":"22957","name":"EvF - B2B Sales&Marketing Conference - JPN - Mar 2017.Invite 1 - ABM Interest","channelId":"429","metrics":[{"name":"Successes","value":"1338"}]},{"id":"17917","name":"Nurture - Asset - How to Create a Lead Nurturing Strategy","channelId":"370","metrics":[{"name":"Successes","value":"1338"}]},{"id":"22216","name":"EmPr - SMB B2C Insightpool Webinar - USA - Dec 2016","channelId":"429","metrics":[{"name":"Successes","value":"1332"}]},{"id":"19585","name":"Website - LaunchPoint: Deskera","channelId":"266","metrics":[{"name":"Successes","value":"1328"}]},{"id":"17009","name":"EvF - Partner Enablement Day - London - EMEA - Mar 2016.Invite - LaunchPoint","channelId":"434","metrics":[{"name":"Successes","value":"1309"}]},{"id":"17189","name":"EmC - Support 3 mo Free - USA - March 2016","channelId":"622","metrics":[{"name":"Successes","value":"1240"}]},{"id":"5724","name":"Social Paid - LinkedIn - Sponsored Updates - EMEA","channelId":"339","metrics":[{"name":"Successes","value":"1233"}]},{"id":"20499","name":"Social Paid - InMail LinkedIn - Virtual Event - APAC Aug 2016","channelId":"339","metrics":[{"name":"Successes","value":"1224"}]},{"id":"18658","name":"WM - JP Marketo Engagement Seminar 0609 - JPN - June 2016.01 - Invite 1","channelId":"429","metrics":[{"name":"Successes","value":"1223"}]},{"id":"15726","name":"EvF - ENT Engagement Marketing Lunch - New York - Feb 2016.Invite 1","channelId":"429","metrics":[{"name":"Successes","value":"1205"}]},{"id":"19256","name":"JPN Web Personalization 101","channelId":"266","metrics":[{"name":"Successes","value":"1198"}]},{"id":"11231","name":"EmSp - B2C FierceRetail - USA - Apr 2015","channelId":"350","metrics":[{"name":"Successes","value":"1196"}]},{"id":"19449","name":"EmPr - Marketing Conquers 4 - APAC - Jul 2016","channelId":"431","metrics":[{"name":"Successes","value":"1153"}]},{"id":"9489","name":"Social Paid - LinkedIn - Sponsored Updates - EMEA - FR","channelId":"339","metrics":[{"name":"Successes","value":"1151"}]},{"id":"19498","name":"EmC - Learning Passport - USA - Jul 2016.ENT Manager L60","channelId":"428","metrics":[{"name":"Successes","value":"1146"}]},{"id":"18870","name":"EvF - Marketo Clinic 0630 - JPN - Jun 2016.Invite 1","channelId":"429","metrics":[{"name":"Successes","value":"1137"}]},{"id":"20932","name":"MP - BAO Opt-In - Manufacturer Opp ID - Q3 2016","channelId":"23","metrics":[{"name":"Successes","value":"1128"}]},{"id":"19513","name":"EvF - JPN Summit RoundTable - JPN - Jul 2016","channelId":"372","metrics":[{"name":"Successes","value":"1094"}]},{"id":"18566","name":"Website - LaunchPoint: Majors, Inc.","channelId":"266","metrics":[{"name":"Successes","value":"1082"}]},{"id":"3732","name":"PPC - Google - EMEA","channelId":"321","metrics":[{"name":"Successes","value":"1077"}]},{"id":"16917","name":"delete Master Intro to Customers","channelId":"566","metrics":[{"name":"Successes","value":"1050"}]},{"id":"15752","name":"Nurture - Asset - DG2MMA","channelId":"371","metrics":[{"name":"Successes","value":"1046"}]},{"id":"17370","name":"PPC - Google Content Marketing Campaign - FR","channelId":"321","metrics":[{"name":"Successes","value":"1008"}]},{"id":"20110","name":"Em - Deal Close - Global - Aug 2016.Customer","channelId":"428","metrics":[{"name":"Successes","value":"1006"}]},{"id":"20912","name":"EmSp - AMI Psychology Digital Marketing - APAC - Sep 2016","channelId":"350","metrics":[{"name":"Successes","value":"1000"}]},{"id":"19257","name":"Website - DG2MMA - JPN","channelId":"266","metrics":[{"name":"Successes","value":"998"}]},{"id":"22657","name":"EvF - Silicon Valley ABM MUG - USA - Mar 2017.Invite 1","channelId":"428","metrics":[{"name":"Successes","value":"995"}]},{"id":"18162","name":"Social Paid - Instagram - Blog - NOAM","channelId":"339","metrics":[{"name":"Successes","value":"979"}]},{"id":"23968","name":"Marketing Nation Summit 2017.Last Call for March - Bay Area - NA (Non-Reg)","channelId":"428","metrics":[{"name":"Successes","value":"966"}]},{"id":"3735","name":"PPC - Google - NOAM","channelId":"321","metrics":[{"name":"Successes","value":"941"}]},{"id":"21274","name":"Nurture - Asset - CS Lifenet JPN","channelId":"371","metrics":[{"name":"Successes","value":"922"}]},{"id":"17824","name":"EvF - Landscape 0418 - JPN - April 2016.Invite 1 - Edit","channelId":"429","metrics":[{"name":"Successes","value":"912"}]},{"id":"17757","name":"VEM - Summit Streaming - May 2016","channelId":"374","metrics":[{"name":"Successes","value":"911"}]},{"id":"21687","name":"EmPr - ENT - Christiana Care Case Study - USA - Nov 2016","channelId":"429","metrics":[{"name":"Successes","value":"911"}]},{"id":"17798","name":"EvL - ENT Fathom Nurture Executive Forum - Apr 2016","channelId":"373","metrics":[{"name":"Successes","value":"899"}]},{"id":"19308","name":"EmPr - ENT B2B - Move Your ABM Plan into Action - APAC - July 2016","channelId":"429","metrics":[{"name":"Successes","value":"882"}]},{"id":"3814","name":"Social Paid - Twitter - NOAM","channelId":"339","metrics":[{"name":"Successes","value":"878"}]},{"id":"17833","name":"EvF - Marketo Pre-Strategy Workshop - Sydney - APAC - Apr 2016.Invite - LaunchPoint","channelId":"434","metrics":[{"name":"Successes","value":"865"}]},{"id":"20501","name":"EvF - Melbourne Cup Day - APAC - Nov 2016.Invite 2","channelId":"429","metrics":[{"name":"Successes","value":"858"}]},{"id":"17815","name":"EmSp - CMI Podcast - USA - Apr 2016","channelId":"350","metrics":[{"name":"Successes","value":"856"}]},{"id":"13351","name":"EmSp - SocialMediopolis - USA - Aug 2015","channelId":"350","metrics":[{"name":"Successes","value":"847"}]},{"id":"20107","name":"EvF - Partner Seminar 0928 - JPN - Sep 2016.Invite 1 - Edit","channelId":"434","metrics":[{"name":"Successes","value":"836"}]},{"id":"22127","name":"WM - ABM Demo - USA - 01/05/17.Invite","channelId":"428","metrics":[{"name":"Successes","value":"830"}]},{"id":"18502","name":"PPC - Google - Lead Nurturing - JPN","channelId":"321","metrics":[{"name":"Successes","value":"824"}]},{"id":"23453","name":"EvF - B2B S&M Follow Up Seminar BtoB - JPN - Mar 2017.Follow Up for Attendees","channelId":"429","metrics":[{"name":"Successes","value":"807"}]},{"id":"18795","name":"EmPr - DG2MA - DE - EMEA - Jun 2016","channelId":"429","metrics":[{"name":"Successes","value":"796"}]},{"id":"17250","name":"EmC - Web Personalization Service - USA - Mar 2016","channelId":"428","metrics":[{"name":"Successes","value":"795"}]},{"id":"22171","name":"EmPr - 20% Referral Partner - APAC - Dec 2016","channelId":"429","metrics":[{"name":"Successes","value":"772"}]},{"id":"22715","name":"EmSp - eMarketer 2 - USA - Jan 2017","channelId":"350","metrics":[{"name":"Successes","value":"769"}]},{"id":"24173","name":"Summit 2017 - Workshop Sessions","channelId":"266","metrics":[{"name":"Successes","value":"761"}]}]}')
		return response
	else:
		return redirect(req.url)

def _proxy(*args, **kwargs):
	resp = requests.request(
		method=request.method,
		url=request.url.replace('http://localhost:5000', 'https://sj-ee-api.marketo.com'),
		headers={key: value for (key, value) in request.headers if key != 'Host'},
		data=request.get_data(),
		cookies=request.cookies,
		allow_redirects=False)
	
	excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
	headers = [(name, value) for (name, value) in resp.raw.headers.items()
						if name.lower() not in excluded_headers]
	
	response = Response(resp.content, resp.status_code, headers)
	return response