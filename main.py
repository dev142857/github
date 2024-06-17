import requests
from bs4 import BeautifulSoup
import re
import csv

numFollower = '100'
searType = 'users'
createdDateMax = '2019-12-31'
createdDateMin = '2000-1-1'
location = 'Canada'
num = 0
pageCount = 0
# get total number of pages
page_url = 'https://github.com/search?q=+followers%3A>%3D'+numFollower+'+created%3A<%3D'+createdDateMax+'+location%3A'+location+'+&type='+searType
try:
    response = requests.get(page_url)
    
    if(response.status_code == 200):
        json_data = response.json()
        pageCount = json_data['payload']['page_count']
        print(pageCount)
except Exception as e:
    print(f"An error occurred from 0: {e}")

# create csv file and define the header
header = ['githubId', 'name', 'Email', 'LinkedIn', 'Location', 'Followers', 'Following', 'CEO', 'CTO', 'Founder', 'co-Founder']
with open(location + '.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    
    for currentPage in range(1, pageCount, 1):
        page_url = 'https://github.com/search?q=+followers%3A>%3D'+numFollower+'+created%3A<%3D'+createdDateMax+'+location%3A'+location+'+&type='+searType+'&p='+str(currentPage)
        num = num+1
        try:
            response = requests.get(page_url)
            
            if(response.status_code == 200):
                json_data = response.json()
                                
                arrMemberData = json_data['payload']['results']
                
                # get the url of each members
                def getMemberUrl(memberData):
                    return memberData['hl_login']
                memberUrls = list(map(getMemberUrl, arrMemberData))
                
                for memberId in memberUrls:
                    member_url = 'https://github.com/' + memberId
                    
                    # cookie info
                    cookies = {
                        'GHCC': 'Required:1-Analytics:1-SocialMedia:1-Advertising:1',
                        'MSFPC': 'GUID=20525d3347da4a19beef4dd42b107fd8&HASH=2052&LV=202406&V=4&LU=1717377975452',
                        'MicrosoftApplicationsTelemetryDeviceId': 'a2063b98-fab1-4986-afa7-74a324938a7c',
                        '__Host-user_session_same_site': 'fE6FHzl9xjxqGvq1M2N-x6Z3TqdhI9g5LOXYM0cyiOQ0rlW5',
                        '_device_id': '5b747db3f631fa757cb88c81a1755468',
                        '_gh_sess': 'SnOZFs6FweGsLsbgzTyVa%2FsbDJlNxA6S5%2FNaV%2FlUG%2FmEmGlK4EIDu7LPkOk7%2BlTDk67hr4wHgYAbNKZcPJhVsiIzxDCPkMPMOYoo4KfbT8tC6CDfZR66eKpkAhiRUDSIaB906Fy0benw4vBxgLHMw5Sd3CDSkcty%2BI8Ti%2FDnaKgqADP5Ft6sUlrT1oiTiFJXYN54wKPN%2F8n1GegeWbdNRH2Sn2BQeSK7fNZ%2BqfnvVw2hdSdR%2BqSCcTA5swOtc3K4ifF01VQiyPRp7Y5%2BKq03tvJ0F1V7jm5eLXZ2Px5k8JIfEsNYVjty0ArZtKIgdkBmsP%2FdtoOsap%2FmyKXXJUdivaxFA%2BjLxEIZ1U1e9%2F8xObrUNS5R2y55TAD1xoF%2BYkT3--hEHO%2BPGSfWldh3Lw--YZKW3merhBNt1pJeD9nG0g%3D%3D',
                        '_octo': 'GH1.1.1849676077.1717050262',
                        'color_mode': '%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D',
                        'dotcom_user': 'dev142857',
                        'has_recent_activity': '1',
                        'logged_in': 'yes',
                        'preferred_color_mode': 'dark',
                        'saved_user_sessions': '152303121%3AfE6FHzl9xjxqGvq1M2N-x6Z3TqdhI9g5LOXYM0cyiOQ0rlW5',
                        'tz': 'America%2FNew_York',
                        'user_session': 'fE6FHzl9xjxqGvq1M2N-x6Z3TqdhI9g5LOXYM0cyiOQ0rlW5',
                    }
                    print(num)
                    try:
                        response = requests.get(member_url, cookies=cookies)
                        if(response.status_code == 200):
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            name = soup.find('span', {'class': 'p-name vcard-fullname d-block overflow-hidden'}).text.strip()
                            
                            mem_location = soup.find('span', {'class': 'p-label'}).text.strip() if soup.find('span', {'class': 'p-label'}) else 'No location specified'
                            
                            info_follow = soup.find_all('span', {'class': 'text-bold color-fg-default'})
                            num_followers = info_follow[0].text
                            num_following = info_follow[1].text
                            
                            email_element = soup.find('a', {'href': lambda x: x and x.startswith('mailto:')})
                            email = email_element['href'][7:] if email_element else ''
                            
                            linkedin_element = soup.find('a', {'href': lambda x: x and x.startswith('https://www.linkedin.com/')})
                            linkedin = linkedin_element['href'] if linkedin_element else ''
                            
                            div_member_detail = soup.find('div', {'class':'p-note user-profile-bio mb-3 js-user-profile-bio f4'})
                            member_detail = div_member_detail.get('data-bio-text', 'No bio specified')
                            def duty_check(duty, is_sens):
                                if is_sens:
                                    if re.search(duty, member_detail):
                                        return True
                                    else:
                                        return False
                                else :
                                    if re.search(duty, member_detail, re.IGNORECASE):
                                        return True
                                    else:
                                        return False
                            is_cto = "CTO" if duty_check("CTO", True) else ""
                            is_ceo = "CEO" if duty_check("CEO", True) else ""
                            is_co_founder = "co-Founder" if duty_check("co-founder", False) else ""
                            is_founder = "Founder" if duty_check("founder", False) and is_co_founder=="" else ""
                            
                            data = [memberId, name, email, linkedin, mem_location, num_followers, num_following, is_ceo, is_cto, is_founder, is_co_founder]
                            writer.writerow(data)       
                        
                    except Exception as e:
                        print(f"An error occured from 1: {e}")            
                
                # print(memberUrls)
        except Exception as e:
            print(f"An error occurred from 2: {e}")
