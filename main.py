import requests
import threading
from queue import Queue
import time

def print_banner():
    banner = """
    ############################################################
    #                                                          #
    #   ██████████████████████████████████████████████████   #
    #   █ ████ ████  ████ ████ ████ ████ ████████ ████   #
    #   █ ████ ████    ████ ██████ █████ ████ ██████ ████  #
    #   ████████████████████████ Admin Panel Finder ████████  #
    #                                                          #
    #  [+] discord:heloqwe        #
    #  [+] admin səhifəsi tapmaq üçün yaradılıb             #
    #  [✔] istifadə etmədən öncə admindən icazə alın         #
    #                                                          #
    ############################################################
    """
    print(banner)

def admin_yollarini_al():
    return [
        '/admin', '/login', '/wp-admin', '/administrator', '/adminpanel', '/controlpanel', 
        '/cpanel', '/user', '/dashboard', '/admin_login', '/signin', '/secure', '/manager', 
        '/settings', '/backend', '/siteadmin', '/cms', '/system', '/config', '/private', 
        '/mainadmin', '/userpanel', '/account', '/member', '/adminarea', '/superadmin', '/auth', 
        '/loginpanel', '/useradmin', '/webadmin', '/adminaccess', '/root', '/access', '/backendadmin', 
        '/sitecontrol', '/adminconsole', '/loginadmin', '/adminpanel1', '/adminlogin', '/admin-area', 
        '/adminaccess', '/super-admin', '/adminsecure', '/loginform', '/control-panel', '/adminarea1', 
        '/cms-admin', '/admin/settings', '/admincp', '/admin_dashboard', '/admin-console', '/adminloginpage', 
        '/admin_config', '/adminpanel1', '/backend-access', '/admin-dashboard', '/admin-console1', 
        '/adminloginform', '/adminpanel2', '/sitecontrolpanel', '/adminpanel3', '/admin-portal', 
        '/admins', '/adminaccesspanel', '/adminloginform1', '/admin-panel-control', '/systempanel', '/admin_web', 
        '/controlpanel-admin', '/root-login', '/adminbackend', '/superadminpanel', '/adminauth', '/adminaccesscontrol', 
        '/adminloginform1', '/adminloginarea', '/adminlogincontrol', '/admin-dashboard1', '/site-login', 
        '/admin-securelogin', '/backendlogin', '/adminloginnew', '/admin-console1', '/admin-loginpage', 
        '/adminconfigpanel', '/adminroot', '/adminpanelaccess', '/adminloginpanel', '/secure-admin', '/admin-login-form', 
        '/adminarea3', '/adminloginpanel1', '/panel-login', '/adminrootlogin', '/superadminpanel1', '/adminlogintest', 
        '/controlaccess', '/adminpanel-advanced', '/admincontrolpanel', '/adminpage1', '/admin_loginpanel', 
        '/useradminpanel', '/backendsystem', '/rootpanel', '/admincpanel', '/paneladmin', '/backend-control', 
        '/site-admin', '/adminsite', '/admin-management', '/secure-login', '/admin-page', '/admin_panel', 
        '/admin-settings', '/manage', '/adminpanel2', '/sitecontrolpanel', '/adminpanel3', '/admin-portal', 
        '/admins', '/adminaccesspanel', '/adminloginform', '/adminpanel-advanced', '/admincontrolpanel', '/adminpage1', 
        '/admin_loginpanel', '/useradminpanel', '/backendsystem', '/rootpanel', '/admincpanel', '/paneladmin', '/backend-control',
        
    ]

def urlu_yoxla(base_url, path, result_queue):
    full_url = base_url.rstrip('/') + path
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Tapıldı: {full_url}")
            result_queue.put(full_url)
        elif response.status_code == 403:
            print(f"[!] Qadağan Olunmuş (403): {full_url}")
        elif response.status_code == 404:
            print(f"[-] Tapılmadı (404): {full_url}")
    except requests.RequestException:
        print(f"[x] Xəta: {full_url}")

def admin_səhifələrini_tar(base_url):
    yollar = admin_yollarini_al()
    result_queue = Queue()
    threads = []

    print(f"Hədəf taranır: {base_url}")
    print("Tarama başlayır...\n")

    for path in yollar:
        t = threading.Thread(target=urlu_yoxla, args=(base_url, path, result_queue))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    tapılan_səhifələr = []
    while not result_queue.empty():
        tapılan_səhifələr.append(result_queue.get())

    return tapılan_səhifələr


if __name__ == "__main__":
    print_banner()
    
    hədəf_url = input("Hədəf vebsaytını daxil edin (məsələn http://example.com): ")
    if not hədəf_url.startswith("http"):
        hədəf_url = "http://" + hədəf_url

    start_time = time.time()
    tapılan_səhifələr = admin_səhifələrini_tar(hədəf_url)
    end_time = time.time()

    print("\n=== Tarama Nəticələri ===")
    if tapılan_səhifələr:
        print("Tapılan admin səhifələri:")
        for page in tapılan_səhifələr:
            print(f"- {page}")
    else:
        print("Heç bir admin səhifəsi tapılmadı.")
    print(f"Tarama müddəti: {end_time - start_time:.2f} saniyə")
