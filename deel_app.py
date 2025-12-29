import json
import re
import csv
import math
import sys
import streamlit as st
from datetime import datetime
from collections import defaultdict

# Streamlit configuration
st.set_page_config(
    page_title="DEEL AI TRANSACTION SYSTEM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #FEE2E2;
        border-left: 4px solid #EF4444;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .transaction-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .json-output {
        background-color: #1E1E1E;
        color: #D4D4D4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin: 1rem 0;
        border: 1px solid #444;
    }
    .json-key {
        color: #9CDCFE;
    }
    .json-string {
        color: #CE9178;
    }
    .json-number {
        color: #B5CEA8;
    }
    .json-boolean {
        color: #569CD6;
    }
    .delete-button {
        background-color: #EF4444 !important;
        color: white !important;
        border: none !important;
    }
    .delete-button:hover {
        background-color: #DC2626 !important;
    }
</style>
""", unsafe_allow_html=True)

def display_json(data, title="JSON Output"):
    """Display JSON data in a formatted way"""
    st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)
    
    # Format JSON with syntax highlighting
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    # Simple syntax highlighting
    json_str = json_str.replace('"', '<span class="json-string">"</span>')
    json_str = json_str.replace(': ', ': <span class="json-key">')
    json_str = json_str.replace(',\n', '</span>,\n')
    json_str = json_str.replace('{\n', '{<br>')
    json_str = json_str.replace('\n}', '<br>}')
    json_str = json_str.replace('\n    ', '<br>    ')
    
    st.markdown(f'<div class="json-output">{json_str}</div>', unsafe_allow_html=True)
    
    # Also provide a download button
    st.download_button(
        label="📥 Download JSON",
        data=json.dumps(data, indent=2, ensure_ascii=False),
        file_name=f"{title.lower().replace(' ', '_')}.json",
        mime="application/json"
    )

class DeelTransactionSystem:
    def __init__(self):
        self.transactions = []
        self.users = []
        self.load_or_create_data()
        
    def load_or_create_data(self):
        """Load data from files or create sample data"""
        try:
            # Load transactions from CSV format
            with open('transactions.csv', 'r', encoding='utf-8') as f:
                first_line = f.readline()
                f.seek(0)
                
                if ',' in first_line:
                    reader = csv.DictReader(f)
                    self.transactions = []
                    for row in reader:
                        amount_str = row.get('amount ($)', '').strip() if 'amount ($)' in row else row.get('amount', '').strip()
                        if not amount_str:
                            for key, value in row.items():
                                if value and value.replace('.', '', 1).isdigit():
                                    amount_str = value
                                    break
                        
                        amount_str = amount_str.replace('$', '').replace(',', '').strip()
                        try:
                            amount = float(amount_str)
                        except:
                            amount = 0.0
                        
                        description = row.get('description', '')
                        if not description:
                            for key, value in row.items():
                                if value and len(value) > 10 and not value.replace('.', '', 1).isdigit():
                                    description = value
                                    break
                        
                        transaction = {
                            'id': row.get('id', ''),
                            'amount': amount,
                            'description': description
                        }
                        self.transactions.append(transaction)
            
            # Load users from CSV format
            with open('users.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.users = []
                for row in reader:
                    user = {
                        'id': row.get('id', ''),
                        'name': row.get('name', ''),
                    }
                    self.users.append(user)
                    
        except FileNotFoundError:
            self.create_sample_data()
            self.save_to_csv()
        except Exception as e:
            self.create_sample_data()
            self.save_to_csv()
    
    def create_sample_data(self):
        """Create sample data using provided data"""
        # transactions data
        self.transactions = [
            {"id": "caqjJtrI", "amount": 88549.0, "description": "From Liam J. Johnson for Deel, ref 4oJnVOMRLZftACC//403705217843//CNTR"},
            {"id": "AcwQVVtq", "amount": 95880.0, "description": "From Olivia Roland Smith for Deel, ref mhH2aFLP4rPTACC//460168509379//CNTR"},
            {"id": "N0wJk7Kp", "amount": 56834.0, "description": "From 杨陈 for Deel, ref 0Ckil9BX0zXMACC//14748849412//CNTR"},
            {"id": "RAZbbmLX", "amount": 98237.0, "description": "Transfer from Emma Brown for Deel, ref kKx5IWycb93DACC//943167654914//CNTR"},
            {"id": "bIzmL3pD", "amount": 82977.0, "description": "From Oliver Talor for Deel, ref zMpiWFssuC1sACC//227441521818//CNTR"},
            {"id": "m1wOOZNz", "amount": 9101.0, "description": "From Ἄλεξις Ava Anderson \ for Deel, ref 05SbIAy2skd RACC//245536464259//CNTR"},
            {"id": "YPOEKpLs", "amount": 74574.0, "description": "From William Martinez for Deel, ref WTrshixkeu1bACC//674187619769//CNTR"},
            {"id": "Ysop2Dzq", "amount": 34224.0, "description": "Received from !Isabel Wilson for Deel, ref MBGqLvH42h86ACC//408322552701//CNTR"},
            {"id": "86OWU7JD", "amount": 69999.0, "description": "From Elijah    Thomas for Deel, ref Ztp4U. cviuBQGACC//464686064210//CNTR"},
            {"id": "ZdNxnh4E", "amount": 63809.0, "description": "From Sophia Lizzie    Clark for Deel, ref FK824HgoLbQWACC//24332722812//CNTR"},
            {"id": "o38UQgrd", "amount": 24600.0, "description": "ref KdlU2gNBe4UkACC//262389856139//CNTR From James. Rodríguez for Deel, "},
            {"id": "J7os8g9d", "amount": 38405.0, "description": "From Mia Lewis, for Deel, ref dAK21Vs4e7vNACC//627987585520//CNTR"},
            {"id": "kXAGOWZ4", "amount": 40781.0, "description": "From Benjamin Lee Test for Deel, ref 9J6Z8JulDKC6ACC//781831470590//CNTR"},
            {"id": "rJfl3qKG", "amount": 2168.0, "description": "Request from Charlotte  Grace Walker for Deel, ref eyQXUXo0VetvACC//599309693244//CNTR"},
            {"id": "KX4Ug0Vd", "amount": 51965.0, "description": "From LucAS Hall for Deel, ref OfyJs95EIEy2ACC//202544590548//CNTR"},
            {"id": "fpFEF1ur", "amount": 72546.0, "description": "From Amelia Turner for Deel, ref JDtWqKRm8XppACC//354138983151CCElijah//CNTR"},
            {"id": "GLLh0V6N", "amount": 46418.0, "description": "Transfer from Hen ry Hill for Deel, ref eY3bFzieZ. 6fDACC//29987282543//CNTR"},
            {"id": "QvW72smG", "amount": 29890.0, "description": "From Harper580Adams for Deel, ref iOOGkNSUx60VACC//702602048415//CNTR"},
            {"id": "uU2NRqif", "amount": 44812.0, "description": "  From Αλέξανδρος Μπέικερ for Deel, ref 5ZbSrAlOvfqDACC//922906239060//CNTR"},
            {"id": "ycH8jf7N", "amount": 72697.0, "description": "From Évèlyn Allèn Jr. for Deel, ref cQqQDAA NGtu4AC a'',adsC//426045068062//CNTR"},
            {"id": "ei6nge4H", "amount": 90425.0, "description": "From Danniel.Wright for Deel, ref 2iWIr1my1oNIACC//826468457411//CNTR"},
            {"id": "jUuibOk8", "amount": 94298.0, "description": "Payment from אֲבִיגַיִל גרין for Deel, ref mBEG9W1jyIj. zACC//252746919478//CNTR"},
            {"id": "772Y58MU", "amount": 21265.0, "description": "From Matthe';w Ki|ng for Deel, ref QikIUvnJPdY8ACC//228449538371//CNTR"},
            {"id": "aglz0x27", "amount": 14591.0, "description": "Payment from Sophia   Cork for Deel, ref dYHRq84OWic3 ACC//596726975562//C NTR"},
            {"id": "YQpsruWK", "amount": 16552.0, "description": "From Michael 60413 Moore for Deel, ref E47q70bJeQAHACC//383849066552//CNTR"},
            {"id": "iLZfczUk", "amount": 3650.0, "description": "Transfer from Elizabeth Nora Mitchell for Deel, ref XsSovxGcE 7yjACC//202297416135//CNTR"},
            {"id": "l8cn5kW7", "amount": 59155.0, "description": "From Jackson for Deel, ref 7eWbcoTyndmdA0,';CC//Nelson662373120171//CNTR"},
            {"id": "bQTK9h5F", "amount": 90940.0, "description": "From   Deel, ref 6o5rMIf23tCLACC//30434. 8221268//CNTR, ref Campbell"},
            {"id": "cJxua5um", "amount": 94177.0, "description": "From Davd # Carter 94177 for Deel, ref 0aQSpCwopTr 0ACC//50280867206//CNTR"},
            {"id": "JkJnn0kt", "amount": 94599.0, "description": "Transfer from 陈剑 for Deel, ref kcg2uswXSae6ACC//270685055935//CNTR, CN"},
            {"id": "BWIigGOK", "amount": 14574.0, "description": "From Joseph Elijah evans for Deel, ref Th1GFHihTX7IACC//674072611669//CNTR"},
            {"id": "mYMQcqtN", "amount": 8252.0, "description": "From Grace COLLINS for Deel, ref ZsE7FSQMJWRZACC//26420273995//CNTR cc Grace"},
            {"id": "Oz12uLqw", "amount": 11517.0, "description": "From Samuel Ewards, ref xY40fJaHfl0pACC//947117080077//CNTR"},
            {"id": "zKzUOlWx", "amount": 79653.0, "description": "From Benjamin Leedsfor Deel, ref n7RgpOBeok6MACC//607317210539//CNTR"},
            {"id": "62O2d9rm", "amount": 60540.0, "description": "Payment from Benjamin Rivera for Deel, ref M0VYem35 # jp80ACC//245929755733//CNTR"},
            {"id": "iMsNYIes", "amount": 27084.0, "description": "From Lily Kelly01 for Deel, ref R61iD7yMOvhLACC//916452734626//CNTR ref Stripe"},
            {"id": "pXAMd74U", "amount": 53576.0, "description": "From for Deel, ref KFRJKAQf3UmwACC//451  230593191//CNTR ref: Jack Cooper"},
            {"id": "1L7kkXTk", "amount": 33134.0, "description": "From 刘王 for Deel, ref iBxqUQgWCQ5xACC//532800242260//CNTR"},
            {"id": "Tn3ParZH", "amount": 27893.0, "description": "From Andrew Richar dson for Deel, ref 3w8t3Cm oKtxHACC//45357314666//CNTR"},
            {"id": "hme4Sohp", "amount": 80990.0, "description": "From Aria Cox for Deel, ref 1XZd   lO0bUAEkACC//722923598131//CNTR"},
            {"id": "kV6qdhZ2", "amount": 83112.0, "description": "To Deel Limited CREDIT REF From Christopher ERR# Ward for Deel, ref lc5CPGXlCbfV ACC//2 3569501332//CNTR"},
            {"id": "mkcUo5Z7", "amount": 52776.0, "description": "Payment from Scarlettross for Deel, ref 3XcqgSiFCLl7ACC//158226484940//CNTR"},
            {"id": "1NfQ59pg", "amount": 97070.0, "description": "From William hillips for Deel, debit ref DIXtzQm5IO0zACC//324137134388//CNTR"},
            {"id": "vUl27SqF", "amount": 49811.0, "description": "From zoeyhowardfor Deel, ref 5azQbS8RncclACC//229632809211//CNTR"},
            {"id": "LToaYEdv", "amount": 40796.0, "description": "  From J for Deel, ref 1pg8kFxI85TxACC//838904646618//CNTR, Foster"},
            {"id": "xgDlc1vd", "amount": 91610.0, "description": "From Refley Hayes for Deel, ref mWJ5iNM R6TW1ACC//343604403820//CNTR"},
            {"id": "K0PvnhYL", "amount": 40952.0, "description": "From Daniel Torres   Smith for Deel, ref 0R5pzL0z2274ACC//844239942124//CNTR"},
            {"id": "H206KrAe", "amount": 2618.0, "description": "From Penelope Campbell for Deel, ref B1Dmdkg   ZQaghAC. C//997618212692//CNTR"},
            {"id": "WfBC5iDR", "amount": 64857.0, "description": "From Richard COLEman for Deel, ref j7iLqKLaAcUHACC//580965106098//CNTR"},
            {"id": "iA9W3i4p", "amount": 13016.0, "description": "Payment from Layla JJ Simmons for Deel, ref MSiATnIekZ8FACC//530393227103//CNTR"},
            {"id": "po2g9Xm7", "amount": 11.0, "description": "Deel payment from Isabella Wilson for Deel, ref f5y6MQuBoDC7ACC//.  522175259477//CNTR Test 2"},
            {"id": "nbu7y4bD", "amount": 33358.0, "description": "From Στέλλα Σάντερς or Deel, ref 9w8klaP6jIXbACC//695030250684//CNTR"},
            {"id": "FIWdSeXw", "amount": 45304.0, "description": "From Joshua Ross for Deel, ref TIAx1Dd 0GqPf ACC//7368 50308280//CNTR"},
            {"id": "bjlYu7Bu", "amount": 24686.0, "description": "From AURORA  POWELL for Deel, ref jk5MU6rT0PipACC//426818621925//CNTR"},
            {"id": "X8TL4dMU", "amount": 482.0, "description": "From Jonathan ,ERR#   perry for Deel, ref HOho3u6fCfA  LACC//1536 84403399//CNTR"},
            {"id": "khe7Al8M", "amount": 97047.0, "description": "From Ellie L0NG for Deel, ref 91be6IO1bT9LACC//117271000422//CNTR"},
            {"id": "lNsyXbbm", "amount": 49227.0, "description": "From Matthewbrooks for Deel, ref V4tS94LUIhnn ACC//133241906791//CNTR"},
            {"id": "YdnIEv4P", "amount": 24893.0, "description": "ref ToCu6iXjX7jMACC//307338080372//CNTR From Hannah Wood for Deel, "},
            {"id": "RGddTMKb", "amount": 72231.0, "description": "From for Deel, ref brclUxkgDQxGACC//  82366915272//CNTR, ref: Samuel Washington "},
            {"id": "kWedRMMj", "amount": 32169.0, "description": "From Hàzèl Fòstèr for Deel, ref IIiBgauTFe2WACC//192898280394//CNTR"},
            {"id": "Ev3RE1ZN", "amount": 53804.0, "description": "Payment from Christopher Morgan for Deel, ref aW7sNT8XG5HEACC//881041028266//CNTR"},
            {"id": "1yiHP6j1", "amount": 70901.0, "description": "From Victoria Fisher for Deel, ref WFzjfQGdZBOWACC//243572413934//CNTR"},
            {"id": "LLNtaY1E", "amount": 31925.0, "description": "Transfer from andrew   barnes for deel, ref CIUzXGzZKjXCACC//96665 0170774//CNTR"},
            {"id": "8CMYRRuJ", "amount": 43452.0, "description": "To Deel, From BeLLA Bennett, Debit for Deel, ref FyVQuiRcC6WOACC//822225184231//CNTR"},
            {"id": "TcK8tATA", "amount": 36079.0, "description": "From David Matthew Hughes for Deel, ref fLMhfb3cblKAACC//601540098907//CNTR"},
            {"id": "TYEUeTqp", "amount": 68228.0, "description": "From Luna LoveReed for Deel, ref NT83w6IxGAA6ACC//245553792376//CNTR"},
            {"id": "QDjbEktD", "amount": 83311.0, "description": "  From GAbriel C for Deel, ref O7vhDWwuF9HwACC//414484851241//CNTR"},
            {"id": "I8WIeHQ2", "amount": 51683.0, "description": "From Mila K Ward for Deel, ref NA2YDcPJiF47A CC//111019096907//CNTR"},
            {"id": "pzXPtaQX", "amount": 50180.0, "description": "From Christopher Gonzal ez 0912 for Deel, ref kzXlB64from Deelvxp4cACC// 136326279819//CNTR"},
            {"id": "ukegCBQf", "amount": 58019.0, "description": "Received from Paisley Taylor for Deel, ref ksIVpU1sRNWsACC//374252501136//CNTR"},
            {"id": "WnU1N3KB", "amount": 9790.0, "description": "From or Deel, ref rw6j3KyBDwN7ACC// John Mitchell 77152073245//CNTR"},
            {"id": "D5aW2I5o", "amount": 7118.0, "description": "From James Bennett. for Deel, ref mRwqP1U katxJACC//83 6081329508//CNTR"},
            {"id": "hqLc27Y0", "amount": 5304.0, "description": "Transfer from Elii, Morris for Deel, ref QtCi92cN8G4uACC//610134600789//CNTR"},
            {"id": "AXLbpmng", "amount": 18640.0, "description": "From Natalie 4Reed for Deel, ref PjwTiDQiNmSxACC//274051933698//CNTR"},
            {"id": "ubfjurUH", "amount": 41553.0, "description": "Payment from Isaac Bell for Deel, ref wNRgWW35i2lSACC//196752583852//CNTR"},
            {"id": "UTtagNiO", "amount": 14313.0, "description": "Transfer from Savannah, Cox for Deel, ref yusBURo0rWCTACC//Wise270331093380//CNTR"},
            {"id": "n9TP2eyH", "amount": 73957.0, "description": "From Samuel Cooper for Deel, ref 78jt3NUhNqb0ACC//234687750024//CNTR"},
            {"id": "Pve1P1JG", "amount": 7471.0, "description": "From Claire.   Simmons for Deel, ref nSQnjQTpx11hACC//852986891535//CNTR"},
            {"id": "pSSoQLp1", "amount": 65498.0, "description": "From Henry for Deel, ref chKWkdineb8KACC//377565502403//CNTR cc Gray"},
            {"id": "mzF8d1xj", "amount": 75846.0, "description": "ref ntTQWJzFuTUcACC//418585662634//CNTR, From Nora Robérts for Deel"},
            {"id": "MKQBCtHk", "amount": 12799.0, "description": "From 李周 for Deel, ref b1e0C1D9L8UBACC//18540590190//CNTR"},
            {"id": "Dh4v16ya", "amount": 25945.0, "description": "From Leah Phillips   for Deel, ref 4Nl53fQgzTLW  ACC//139343615978//CNTR"},
            {"id": "FvlVMfTK", "amount": 77075.0, "description": "Received from Christian Ridley Scott for Deel, ref 3IF2b0AC palNACC//135548234898//CNTR"},
            {"id": "HA7WvqW8", "amount": 11629.0, "description": "From Skylarrichardson for Deel, ref 7kyzcadBHmcPACC//312395299071//CNTR"},
            {"id": "NeK3bkCl", "amount": 7754.0, "description": "From Daniel Rivera for Deel, ref eMIPKJK8o96oACC//6991339   43862//CNTR"},
            {"id": "guxUF6y3", "amount": 91642.0, "description": "From Audrey Watson for Deel, ref yOt958gn  x5ihACC//993136471955//CNTR"},
            {"id": "JL0D4qb8", "amount": 71015.0, "description": "From Matthew RogersWest for Deel, ref 41FhWzvdPr0wACC//786114371221//CNTR"},
            {"id": "QHT6WjtE", "amount": 92402.0, "description": "ref 41FhWzvdPr0wACC//781928311221//CNTR"},
            {"id": "cbkyilio", "amount": 76097.0, "description": "To Deel From Ανδρέας Ροντέελ for Deel, ref JWpKX08r58TFACC//320031128372//CNTR"},
            {"id": "z9sxWMp1", "amount": 76933.0, "description": "From Addison, Hughes for Deel, ref 3QJqWKnphs7gACC//576214218838//CNTR"},
            {"id": "dkNXQFOr", "amount": 6571.0, "description": "From David . Wood for Deel, ref 71TzDTannTpqACC//912938527393//CNTR, CC Isabella P Wilson"},
            {"id": "OuFHALqM", "amount": 3773.0, "description": " ref 3Klmiksre3kcACC//824788665387//CNTR, from Lily, Foster for Deel,"},
            {"id": "Flmxgl6m", "amount": 53048.0, "description": "From James K Coleman for Deel, ref 5f2Lv5I4F6I0ACC//786232316420//CNTR"},
            {"id": "kAHSbQVZ", "amount": 41438.0, "description": "Payment from   Coleman Elliefor Deel, ref xA6yX5UBYJDIACC//70625  4192680//CNTR"},
            {"id": "73or0URj", "amount": 68213.0, "description": "From ERR# Ryan Diaz for Deel, ref VN5wa5wfSbbtACC//447264510603//CNTR"},
            {"id": "SxybKXAR", "amount": 75557.0, "description": "From Audrey Peterson for Deel, ref UWSpnVhFXGHsACC//591757440683//CNTR"},
            {"id": "Q70YUP0y", "amount": 25949.0, "description": "Transfer from  奕辰 for Deel, ref 7bQYUZ1Bble5ACC//852295144198//CNTR"},
            {"id": "9BXRliwT", "amount": 88333.0, "description": "From Elena## BUTLET for Deel, ref oheOEVx,wfB1XACC//169992916947//CNTR"},
            {"id": "5iXzRftq", "amount": 54600.0, "description": "From Christian Griffin for Deel, ref NAJRqF8WtAndACC//808417184144//CNTR"},
            {"id": "D3k1gB6S", "amount": 76571.0, "description": "From Grace Henderson for Deel, ref odjYain0Nn65ACC//623238516454//CNTR"}
        ]
        
        # users data
        self.users = [
            {"id": "0SIPZjNuoc", "name": "David Wood"},
            {"id": "2xmcoVivzb", "name": "Sophia Cork"},
            {"id": "4qkOzbyv8T", "name": "Chris Gonzalez"},
            {"id": "55Gm68Ccwt", "name": "Evelyn Allen"},
            {"id": "5V675CF26e", "name": "Alexis Anderson"},
            {"id": "5WNEypC0m3", "name": "Benjamin Leeds"},
            {"id": "6EMyCbDRkP", "name": "Stella Sanders"},
            {"id": "6fc89iJwho", "name": "Isaac Bell Deel"},
            {"id": "6qpOLRLwjT", "name": "Sophia Elizabeth Clark"},
            {"id": "79vkUflfMg", "name": "John Ryan Diaz"},
            {"id": "79xW1adz5g", "name": "Jian Chen"},
            {"id": "7q68zSaFTx", "name": "Sam Cooper"},
            {"id": "7wgTardvTI", "name": "Penelop Campbell"},
            {"id": "7xElNaaCQk", "name": "Liu Wang"},
            {"id": "8aq20vZEdJ", "name": "Jack Cooper"},
            {"id": "8Habsd7CTg", "name": "Elena"},
            {"id": "8rb7GnSzJk", "name": "Audrey Eleanor Peterson"},
            {"id": "8ux42Wpbip", "name": "Savannah Cox"},
            {"id": "AMll2cfBB3", "name": "Aria J Cox"},
            {"id": "biQokkjAng", "name": "Sam Edwards"},
            {"id": "bqrLHl0t2x", "name": "Elizabeth Mitchell"},
            {"id": "BuCoIvL79A", "name": "Emma Brown"},
            {"id": "CphJKL9Xdi", "name": "Oliver Taylor"},
            {"id": "crHOEW9iLZ", "name": "Audrey  "},
            {"id": "cvsmvo6HvW", "name": "Jackson Nelson"},
            {"id": "dLq0apeuqQ", "name": "Sophia Campbell"},
            {"id": "DMExRDkob0", "name": "Lily Foster"},
            {"id": "EaZFAk1T5c", "name": "Benjamin Lee"},
            {"id": "FhRDVhmleA", "name": "Daniel Deel"},
            {"id": "FHyv02SXtt", "name": "Daniel Wright"},
            {"id": "Fmq8FMWLvG", "name": "Mila Ward"},
            {"id": "FOaJDAtIsk", "name": "Gabriel Cooper"},
            {"id": "hEXLwnpXdz", "name": "Nora Roberts"},
            {"id": "Hl7n5MGoJo", "name": "Andrew Rodeel"},
            {"id": "HPkVoiDiMh", "name": "Harper Adams"},
            {"id": "HuSxJ0Xpw5", "name": "John Mitchell"},
            {"id": "i52RbjL6om", "name": "AuroraPowell", },
            {"id": "IGGyBnhJMc", "name": "Nathalie Claire Reed"},
            {"id": "IlCknvAtTl", "name": "Matthew King"},
            {"id": "IYkWtGZXLe", "name": "Matthew Brookers"},
            {"id": "IzXzXqM6Kd", "name": "William Phillips"},
            {"id": "J2a9tmnIgt", "name": "Andrew Barnes"},
            {"id": "JaLd6Pqhpr", "name": "Henry Hill"},
            {"id": "Jco6EIdzNx", "name": "Ellie Colman"},
            {"id": "jGcUAiKPn2", "name": "David Carter"},
            {"id": "JhAc0o2nWx", "name": "Christian Ridley Scott"},
            {"id": "K0yjPXISO6", "name": "William James Martinez"},
            {"id": "Kb1GVgxraJ", "name": "Hazel Foster"},
            {"id": "kelsFH8kye", "name": "Yichen"},
            {"id": "kL1f4iVK0i", "name": "Li Zhou"},
            {"id": "lIO4js3kkx", "name": "James L Coleman"},
            {"id": "LpQg45AveB", "name": "Grace Collins"},
            {"id": "lVGwIjbyuF", "name": "Grace H"},
            {"id": "lYkiV5XrpZ", "name": "Rick Coleman"},
            {"id": "McA5Obtn0B", "name": "Layla Simmons"},
            {"id": "NG9mBbhEWZ", "name": "Avigail Green"},
            {"id": "nHDyCE2JUS", "name": "Skylar Richardson"},
            {"id": "nZMQ1GyJ2N", "name": "Yang Chen"},
            {"id": "OTMJ5TCHKM", "name": "Samuel Washington"},
            {"id": "owAZX0Uiq4", "name": "Amelia Turner"},
            {"id": "P6bIUUtNdd", "name": "Henry Gray"},
            {"id": "pdVS8wvwjA", "name": "Paisley Taylor"},
            {"id": "pHRIGzvS2p", "name": "Joseph Evans"},
            {"id": "PYbDvqF2gL", "name": "Eli Morris"},
            {"id": "PZ5gUNWL7O", "name": "Luna Reed"},
            {"id": "qBCElYF454", "name": "Andrw Richardson"},
            {"id": "QP6hL6v0oF", "name": "Matthew West"},
            {"id": "r2ZDOIfIIP", "name": "Scarlett Ross"},
            {"id": "ri78o203V0", "name": ""},
            {"id": "rqUvaPdEyD", "name": "Refley Hayes"},
            {"id": "S9rhnsCPxy", "name": "Lea Phillips"},
            {"id": "SB1zc80PFp", "name": "Olivia North Smith"},
            {"id": "ToAD2rzvGA", "name": "Isabella Wilson"},
            {"id": "TRBJYTbOHR", "name": "Christopher Ward Morgan"},
            {"id": "U4NNQUQIeE", "name": "Liam Johnson"},
            {"id": "U4Pps5wQzx", "name": "Addison James Hughes"},
            {"id": "u8yJD9cFLB", "name": "Joseph Foster"},
            {"id": "UmmrJMw1go", "name": "Daniel Torres"},
            {"id": "UmTNYD8XrY", "name": "Zoey Howard"},
            {"id": "uRCvdelpFs", "name": "Hannah Woods"},
            {"id": "V86OZUmxdr", "name": "Jonathan Perry"},
            {"id": "VfY9DmIkiL", "name": "Isabella Wilson"},
            {"id": "vPYeL2gRtJ", "name": "Charlotte Walker"},
            {"id": "VTkSTucYgz", "name": "David Hughes"},
            {"id": "w9eCGb5eot", "name": "Fisher Victoria"},
            {"id": "WfNEYEo6vu", "name": "Michael Moore"},
            {"id": "WH2fpHdEDk", "name": "Claire Simmons"},
            {"id": "woUGau09yc", "name": "Benjamin Rivera"},
            {"id": "wvbZFCcalJ", "name": "Lucas Hall"},
            {"id": "XSwFsQlyYa", "name": "James Bennett"},
            {"id": "xuLP9ZRIlC", "name": "Alexander Baker"},
            {"id": "XUMMkD3fvH", "name": "James Rodriguez"},
            {"id": "YAKhwLcHLA", "name": "Ellie Long"},
            {"id": "yDhnGNLelf", "name": "Ma Lewis"},
            {"id": "YEYnQomP3u", "name": "Elijah Thomas"},
            {"id": "yiVnc6cMMB", "name": "Griffin Christian"},
            {"id": "Yt4Ppnjbpw", "name": "Christopher Ward"},
            {"id": "Z5Zh6jVQaB", "name": "Lily Kelly"},
            {"id": "ZjCI84CW6U", "name": "Bella Bennett"},
            {"id": "Zq05LEibbQ", "name": "Ross Joshua"},
            {"id": "Qg12EWasd", "name": "Μarιa Perikleous"}
        ]
    
    def save_to_csv(self):
        """Save data to CSV files"""
        # Save transactions
        with open('transactions.csv', 'w', newline='', encoding='utf-8') as f:
            f.write("id,amount ($),description\n")
            for t in self.transactions:
                desc = t['description'].replace('"', '""')
                if ',' in desc or '"' in desc:
                    desc = f'"{desc}"'
                f.write(f"{t['id']},{t['amount']},{desc}\n")
        
        # Save users
        with open('users.csv', 'w', newline='', encoding='utf-8') as f:
            f.write("id,name\n")
            for u in self.users:
                f.write(f"{u['id']},{u['name']}\n")
    
    def extract_name_from_text(self, text):
        """Extract name from text - enhanced for your data format"""
        if not text:
            return ""
        
        text = text.replace('  ', ' ').replace('   ', ' ').strip()
        
        patterns = [
            r'From\s+([^,]+?)\s+for\s+Deel',
            r'from\s+([^,]+?)\s+for\s+Deel',
            r'Transfer from\s+([^,]+?)\s+for\s+Deel',
            r'Payment from\s+([^,]+?)\s+for\s+Deel',
            r'Received from\s+([^,]+?)\s+for\s+Deel',
            r'Request from\s+([^,]+?)\s+for\s+Deel',
            r'To Deel.*From\s+([^,]+?)\s+for\s+Deel',
            r'Deel payment from\s+([^,]+?)\s+for\s+Deel',
            r'From\s+([^,]+?)\s+,\s+for\s+Deel',
            r'From\s+([^,]+?)\s+,\s+ref.*for\s+Deel',
            r'From\s+([^,]+?)\s+ref.*for\s+Deel',
            r'ref.*From\s+([^,]+?)\s+for\s+Deel'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                name = re.sub(r'[^\w\s\.\-]', ' ', name)
                name = re.sub(r'\s+', ' ', name).strip()
                
                name = re.sub(r'\s+\d+$', '', name)
                name = re.sub(r'\s+(jr|sr|ii|iii|iv|test|debit|credit|err#)$', '', name, flags=re.IGNORECASE)
                
                words = name.split()
                if len(words) >= 2:
                    return f"{words[0]} {words[-1]}"
                elif len(words) == 1:
                    return words[0]
                else:
                    return name
        
        name_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    if len(match.split()) >= 2 and len(match) > 5:
                        return match
        
        return ""
    
    def calculate_name_similarity(self, name1, name2):
        """Calculate similarity between two names"""
        if not name1 or not name2:
            return 0.0
        
        n1 = name1.lower().strip()
        n2 = name2.lower().strip()
        
        if n1 == n2:
            return 1.0
        
        words1 = set(re.findall(r'[a-z]+', n1))
        words2 = set(re.findall(r'[a-z]+', n2))
        
        if not words1 or not words2:
            return 0.0
        
        common_words = words1.intersection(words2)
        all_words = words1.union(words2)
        word_similarity = len(common_words) / len(all_words) if all_words else 0.0
        
        chars1 = set(n1.replace(' ', ''))
        chars2 = set(n2.replace(' ', ''))
        common_chars = chars1.intersection(chars2)
        all_chars = chars1.union(chars2)
        char_similarity = len(common_chars) / len(all_chars) if all_chars else 0.0
        
        score = (word_similarity * 0.7) + (char_similarity * 0.3)
        
        if n1 and n2 and n1[0] == n2[0]:
            score += 0.1
        
        if ' ' in n1 and ' ' in n2:
            last1 = n1.split()[-1]
            last2 = n2.split()[-1]
            if last1 == last2:
                score += 0.2
        
        return min(1.0, score)
    
    def find_user_matches_for_transaction(self, transaction_input):
        """Find matching users for a transaction"""
        try:
            transaction = None
            for t in self.transactions:
                if str(t['id']).strip().lower() == str(transaction_input).strip().lower():
                    transaction = t
                    break
            
            if transaction:
                description = transaction['description']
                extracted_name = self.extract_name_from_text(description)
            else:
                description = transaction_input
                extracted_name = self.extract_name_from_text(description)
                transaction = {"id": "User Input", "description": description}
        
        except Exception as e:
            description = transaction_input
            extracted_name = self.extract_name_from_text(description)
            transaction = {"id": "User Input", "description": description}
        
        if not extracted_name:
            return [], "No name could be extracted from description", transaction
        
        matches = []
        for user in self.users:
            if not user.get('name'):
                continue
                
            similarity = self.calculate_name_similarity(extracted_name, user['name'])
            
            if similarity >= 0.3:
                matches.append({
                    'id': user['id'],
                    'name': user['name'],
                    'match_metric': round(similarity, 3)
                })
        
        matches.sort(key=lambda x: x['match_metric'], reverse=True)
        return matches, extracted_name, transaction
    
    def find_similar_transactions(self, query_text, threshold=0.2, top_k=5):
        """Find transactions similar to query text"""
        if not query_text:
            return [], 0
        
        tokens = re.findall(r'\b\w+\b', query_text.lower())
        token_count = len(tokens)
        
        if token_count == 0:
            return [], 0
        
        query_words = set(tokens)
        results = []
        
        for t in self.transactions:
            desc_tokens = re.findall(r'\b\w+\b', t['description'].lower())
            desc_words = set(desc_tokens)
            
            if query_words and desc_words:
                common_words = query_words.intersection(desc_words)
                all_words = query_words.union(desc_words)
                similarity = len(common_words) / len(all_words) if all_words else 0.0
            else:
                similarity = 0.0
            
            if similarity >= threshold:
                embedding = []
                for word in list(query_words)[:10]:
                    embedding.append(1 if word in common_words else 0)
                
                while len(embedding) < 10:
                    embedding.append(0)
                
                results.append({
                    'id': t['id'],
                    'description': t['description'],
                    'amount': t['amount'],
                    'embedding': embedding[:10],
                    '_similarity': similarity
                })
        
        results.sort(key=lambda x: x['_similarity'], reverse=True)
        results = results[:top_k]
        
        for r in results:
            del r['_similarity']
        
        return results, token_count
    
    def add_new_transaction(self, amount, description):
        """Add a new transaction"""
        # Get all numeric IDs
        numeric_ids = []
        for t in self.transactions:
            if t['id'] and t['id'].isdigit():
                numeric_ids.append(int(t['id']))
        
        # Generate new ID
        if numeric_ids:
            new_id = str(max(numeric_ids) + 1)
        else:
            new_id = "1001"
        
        new_transaction = {
            'id': new_id,
            'amount': float(amount),
            'description': description
        }
        
        # Add to transactions list
        self.transactions.append(new_transaction)
        # Save to CSV
        self.save_to_csv()
        
        # Update session state
        if 'system' in st.session_state:
            st.session_state.system.transactions = self.transactions
        
        # Update the system info in session state
        if 'last_transaction_count' in st.session_state:
            st.session_state.last_transaction_count = len(self.transactions)
        
        return new_id, new_transaction
    
    def add_new_user(self, name):
        """Add a new user"""
        # Get all numeric parts from existing IDs
        numeric_ids = []
        for u in self.users:
            if u['id']:
                # Extract numbers from ID
                numbers = re.findall(r'\d+', u['id'])
                if numbers:
                    numeric_ids.extend([int(n) for n in numbers])
        
        # Generate new ID
        if numeric_ids:
            new_num = max(numeric_ids) + 1
        else:
            new_num = 1001
        
        new_id = f"USER{new_num}"
        
        new_user = {
            'id': new_id,
            'name': name
        }
        
        # Add to users list
        self.users.append(new_user)
        # Save to CSV
        self.save_to_csv()
        
        # Update session state
        if 'system' in st.session_state:
            st.session_state.system.users = self.users
        
        # Update the system info in session state
        if 'last_user_count' in st.session_state:
            st.session_state.last_user_count = len(self.users)
        
        return new_id
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID"""
        for i, transaction in enumerate(self.transactions):
            if transaction['id'] == transaction_id:
                deleted_transaction = self.transactions.pop(i)
                self.save_to_csv()
                
                # Update session state
                if 'system' in st.session_state:
                    st.session_state.system.transactions = self.transactions
                
                # Update the system info in session state
                if 'last_transaction_count' in st.session_state:
                    st.session_state.last_transaction_count = len(self.transactions)
                
                return True, deleted_transaction
        return False, None
    
    def delete_user(self, user_id):
        """Delete a user by ID"""
        for i, user in enumerate(self.users):
            if user['id'] == user_id:
                deleted_user = self.users.pop(i)
                self.save_to_csv()
                
                # Update session state
                if 'system' in st.session_state:
                    st.session_state.system.users = self.users
                
                # Update the system info in session state
                if 'last_user_count' in st.session_state:
                    st.session_state.last_user_count = len(self.users)
                
                return True, deleted_user
        return False, None

def main():
    """Main Streamlit App"""
    
    # Initialize session state
    if 'system' not in st.session_state:
        st.session_state.system = DeelTransactionSystem()
    
    # Initialize form states
    if 'add_user_submitted' not in st.session_state:
        st.session_state.add_user_submitted = False
    if 'add_transaction_submitted' not in st.session_state:
        st.session_state.add_transaction_submitted = False
    if 'new_user_data' not in st.session_state:
        st.session_state.new_user_data = None
    if 'new_transaction_data' not in st.session_state:
        st.session_state.new_transaction_data = None
    
    # Store current counts in session state for immediate updates
    if 'last_transaction_count' not in st.session_state:
        st.session_state.last_transaction_count = len(st.session_state.system.transactions)
    if 'last_user_count' not in st.session_state:
        st.session_state.last_user_count = len(st.session_state.system.users)
    
    system = st.session_state.system
    
    # Sidebar Navigation
    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1E3A8A;'>🤖 DEEL AI</h1>
        <p style='color: #6B7280;'>Transaction System</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Task 1: Find Matching Users", "Task 2: Find Similar Transactions", 
         "Add Transaction", "Add User", "Delete Transaction", "Delete User",
         "View Transactions", "View Users", "Statistics", "Demo"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### System Info")
    
    # Update counts in session state if they've changed
    current_transaction_count = len(system.transactions)
    current_user_count = len(system.users)
    
    # Store the current counts in session state for next render
    st.session_state.last_transaction_count = current_transaction_count
    st.session_state.last_user_count = current_user_count
    
    # Display metrics with updated counts
    st.sidebar.metric("Total Transactions", current_transaction_count)
    st.sidebar.metric("Total Users", current_user_count)
    
    # Reset form states when navigating away from forms
    if menu not in ["Add Transaction", "Add User"]:
        st.session_state.add_user_submitted = False
        st.session_state.add_transaction_submitted = False
    
    # Main Content Area
    if menu == "Dashboard":
        st.markdown("<h1 class='main-header'>🤖 DEEL AI TRANSACTION SYSTEM</h1>", unsafe_allow_html=True)
        st.markdown("<h3 class='sub-header'>Complete Web-Based Solution</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h3>📊 Total Amount</h3>
                <h2>${:,.2f}</h2>
            </div>
            """.format(sum(t['amount'] for t in system.transactions)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h3>📈 Avg Transaction</h3>
                <h2>${:,.2f}</h2>
            </div>
            """.format(sum(t['amount'] for t in system.transactions)/len(system.transactions) if system.transactions else 0), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-card'>
                <h3>👥 Active Users</h3>
                <h2>{}</h2>
            </div>
            """.format(len(system.users)), unsafe_allow_html=True)
        
        st.markdown("<div class='success-box'>✅ System Initialized Successfully!</div>", unsafe_allow_html=True)
        
        # Show JSON button for dashboard data
        if st.button("📊 Show Dashboard Data in JSON", key="dashboard_json"):
            dashboard_data = {
                "system_summary": {
                    "total_transactions": len(system.transactions),
                    "total_users": len(system.users),
                    "total_amount": sum(t['amount'] for t in system.transactions),
                    "average_transaction": sum(t['amount'] for t in system.transactions)/len(system.transactions) if system.transactions else 0
                },
                "recent_transactions": [
                    {
                        "id": t['id'],
                        "amount": t['amount'],
                        "description": t['description']
                    } for t in system.transactions[-5:]
                ]
            }
            display_json(dashboard_data, "Dashboard Data")
        
        # Recent Transactions
        st.markdown("<h3 class='sub-header'>Recent Transactions</h3>", unsafe_allow_html=True)
        if system.transactions:
            recent_transactions = system.transactions[-5:]
            for t in recent_transactions:
                with st.expander(f"Transaction {t['id']} - ${t['amount']:.2f}"):
                    st.write(f"**Description:** {t['description']}")
                    st.write(f"**Amount:** ${t['amount']:.2f}")
    
    elif menu == "Task 1: Find Matching Users":
        st.markdown("<h1 class='main-header'>🎯 Task 1: Find Matching Users</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Search by Transaction ID", "Search by Description"])
        
        with tab1:
            st.markdown("<h3 class='sub-header'>Search by Transaction ID</h3>", unsafe_allow_html=True)
            transaction_id = st.text_input("Enter Transaction ID:")
            
            if st.button("Find Matches", key="search_id"):
                if transaction_id:
                    with st.spinner("Searching for matches..."):
                        matches, extracted_name, transaction = system.find_user_matches_for_transaction(transaction_id)
                        
                        if isinstance(matches, list):
                            if matches:
                                st.markdown(f"""
                                <div class='info-box'>
                                    <strong>Extracted Name:</strong> {extracted_name}<br>
                                    <strong>Matches Found:</strong> {len(matches)}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown("<h3 class='sub-header'>Matching Users</h3>", unsafe_allow_html=True)
                                
                                for i, match in enumerate(matches[:10], 1):
                                    with st.container():
                                        col1, col2, col3 = st.columns([3, 2, 1])
                                        with col1:
                                            st.write(f"**{match['name']}**")
                                        with col2:
                                            st.write(f"ID: {match['id']}")
                                        with col3:
                                            st.metric("Match Score", f"{match['match_metric']:.3f}")
                                        st.progress(match['match_metric'])
                                
                                # Show JSON output
                                st.markdown("<h3 class='sub-header'>JSON Output</h3>", unsafe_allow_html=True)
                                json_output = {
                                    "transaction_id": transaction_id,
                                    "transaction_description": transaction['description'] if 'description' in transaction else "",
                                    "extracted_name": extracted_name,
                                    "total_matches": len(matches),
                                    "matches": [
                                        {
                                            "user_id": m["id"],
                                            "user_name": m["name"],
                                            "match_score": m["match_metric"]
                                        } for m in matches
                                    ]
                                }
                                display_json(json_output, "Matching Users Result")
                            else:
                                st.warning("No matching users found.")
                        else:
                            st.error(f"Error: {matches}")
                else:
                    st.warning("Please enter a Transaction ID")
        
        with tab2:
            st.markdown("<h3 class='sub-header'>Search by Description</h3>", unsafe_allow_html=True)
            description = st.text_area("Enter Transaction Description:", height=100)
            
            if st.button("Find Matches", key="search_desc"):
                if description:
                    with st.spinner("Searching for matches..."):
                        matches, extracted_name, transaction = system.find_user_matches_for_transaction(description)
                        
                        if isinstance(matches, list):
                            if matches:
                                st.markdown(f"""
                                <div class='info-box'>
                                    <strong>Extracted Name:</strong> {extracted_name}<br>
                                    <strong>Matches Found:</strong> {len(matches)}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                df_data = []
                                for match in matches[:20]:
                                    df_data.append({
                                        "Rank": len(df_data) + 1,
                                        "User ID": match['id'],
                                        "Name": match['name'],
                                        "Match Score": f"{match['match_metric']:.3f}"
                                    })
                                
                                st.dataframe(df_data, use_container_width=True)
                                
                                # Show JSON output
                                st.markdown("<h3 class='sub-header'>JSON Output</h3>", unsafe_allow_html=True)
                                json_output = {
                                    "search_description": description,
                                    "extracted_name": extracted_name,
                                    "total_matches": len(matches),
                                    "matches": [
                                        {
                                            "rank": i+1,
                                            "user_id": m["id"],
                                            "user_name": m["name"],
                                            "match_score": m["match_metric"]
                                        } for i, m in enumerate(matches)
                                    ]
                                }
                                display_json(json_output, "Matching Users Result")
                            else:
                                st.warning("No matching users found.")
                        else:
                            st.error(f"Error: {matches}")
                else:
                    st.warning("Please enter a description")
    
    elif menu == "Task 2: Find Similar Transactions":
        st.markdown("<h1 class='main-header'>🔍 Task 2: Find Similar Transactions</h1>", unsafe_allow_html=True)
        
        query = st.text_input("Enter search query:")
        
        col1, col2 = st.columns(2)
        with col1:
            threshold = st.slider("Similarity Threshold", 0.1, 1.0, 0.2, 0.1)
        with col2:
            top_k = st.slider("Max Results", 1, 20, 5)
        
        if st.button("Search Similar Transactions"):
            if query:
                with st.spinner("Searching for similar transactions..."):
                    results, token_count = system.find_similar_transactions(query, threshold, top_k)
                    
                    st.markdown(f"""
                    <div class='info-box'>
                        <strong>Query:</strong> {query}<br>
                        <strong>Tokens Found:</strong> {token_count}<br>
                        <strong>Results Found:</strong> {len(results)}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if results:
                        for i, result in enumerate(results, 1):
                            with st.expander(f"Result {i}: Transaction {result['id']} - ${result['amount']:.2f}"):
                                st.write(f"**Description:** {result['description']}")
                                st.write(f"**Amount:** ${result['amount']:.2f}")
                                st.write(f"**Embedding:** {result['embedding']}")
                        
                        # Show JSON output
                        st.markdown("<h3 class='sub-header'>JSON Output</h3>", unsafe_allow_html=True)
                        json_output = {
                            "query": query,
                            "search_parameters": {
                                "similarity_threshold": threshold,
                                "max_results": top_k
                            },
                            "token_count": token_count,
                            "total_results": len(results),
                            "results": [
                                {
                                    "rank": i+1,
                                    "transaction_id": r["id"],
                                    "amount": r["amount"],
                                    "description": r["description"],
                                    "embedding": r["embedding"]
                                } for i, r in enumerate(results)
                            ]
                        }
                        display_json(json_output, "Similar Transactions Result")
                    else:
                        st.warning("No similar transactions found.")
            else:
                st.warning("Please enter a search query")
    
    elif menu == "Add Transaction":
        st.markdown("<h1 class='main-header'>➕ Add New Transaction</h1>", unsafe_allow_html=True)
        
        # Check if we should show the form or the success message
        if not st.session_state.add_transaction_submitted:
            # Use a form key to track submissions
            form_key = "add_transaction_form"
            
            with st.form(key=form_key):
                amount = st.number_input("Amount ($)", min_value=0.01, value=100.0, step=1.0, key="amount_input")
                description = st.text_area("Description", height=100, key="desc_input")
                submit = st.form_submit_button("Add Transaction")
                
                if submit:
                    if amount and description:
                        with st.spinner("Adding transaction..."):
                            new_id, new_transaction = system.add_new_transaction(amount, description)
                            
                            # Store result in session state
                            st.session_state.new_transaction_data = {
                                'transaction_id': new_id,
                                'amount': amount,
                                'description': description,
                                'matches': system.find_user_matches_for_transaction(description)[0],
                                'extracted_name': system.find_user_matches_for_transaction(description)[1]
                            }
                            st.session_state.add_transaction_submitted = True
                            
                            # Force a rerun to update sidebar and show success
                            st.rerun()
                    else:
                        st.error("Please fill all fields")
        else:
            # Show success message and details
            if st.session_state.new_transaction_data:
                trans_data = st.session_state.new_transaction_data
                
                st.markdown("<h3 class='sub-header'>Transaction Added Successfully!</h3>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class='success-box'>
                    ✅ Transaction added successfully!<br>
                    <strong>ID:</strong> {trans_data['transaction_id']}<br>
                    <strong>Amount:</strong> ${trans_data['amount']:.2f}<br>
                    <strong>Description:</strong> {trans_data['description']}
                </div>
                """, unsafe_allow_html=True)
                
                # Find matches for new transaction
                st.markdown("<h3 class='sub-header'>Matching Users</h3>", unsafe_allow_html=True)
                matches = trans_data['matches']
                extracted_name = trans_data['extracted_name']
                
                if matches:
                    st.write(f"Extracted name: **{extracted_name}**")
                    for match in matches[:3]:
                        st.write(f"- {match['name']} (Match: {match['match_metric']:.3f})")
                else:
                    st.info("No matching users found.")
                
                # Show JSON output
                st.markdown("<h3 class='sub-header'>Transaction JSON</h3>", unsafe_allow_html=True)
                transaction_json = {
                    "transaction_added": True,
                    "transaction_id": trans_data['transaction_id'],
                    "transaction_details": {
                        'id': trans_data['transaction_id'],
                        'amount': trans_data['amount'],
                        'description': trans_data['description']
                    },
                    "extracted_name": extracted_name,
                    "matching_users": [
                        {
                            "user_id": m["id"],
                            "user_name": m["name"],
                            "match_score": m["match_metric"]
                        } for m in matches[:5]
                    ]
                }
                display_json(transaction_json, "New Transaction Result")
                
                # Show updated count
                st.info(f"**Total transactions now:** {len(system.transactions)}")
                
                # Add buttons to add another or go back
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("➕ Add Another Transaction"):
                        st.session_state.add_transaction_submitted = False
                        st.session_state.new_transaction_data = None
                        st.rerun()
                with col2:
                    if st.button("🏠 Go to Dashboard"):
                        st.session_state.add_transaction_submitted = False
                        st.session_state.new_transaction_data = None
                        # Navigate to dashboard by changing the menu selection
                        # We can't directly change the sidebar, so we'll show a message
                        st.info("Please select 'Dashboard' from the sidebar")
            else:
                st.error("Error: No transaction data found")
    
    elif menu == "Add User":
        st.markdown("<h1 class='main-header'>👤 Add New User</h1>", unsafe_allow_html=True)
        
        # Check if we should show the form or the success message
        if not st.session_state.add_user_submitted:
            # Use a form key to track submissions
            form_key = "add_user_form"
            
            with st.form(key=form_key):
                name = st.text_input("Full Name", key="name_input")
                submit = st.form_submit_button("Add User")
                
                if submit:
                    if name:
                        with st.spinner("Adding user..."):
                            new_id = system.add_new_user(name)
                            
                            # Store result in session state
                            st.session_state.new_user_data = {
                                'user_id': new_id,
                                'user_name': name
                            }
                            st.session_state.add_user_submitted = True
                            
                            # Force a rerun to update sidebar and show success
                            st.rerun()
                    else:
                        st.error("Please enter a name")
        else:
            # Show success message and details
            if st.session_state.new_user_data:
                user_data = st.session_state.new_user_data
                
                st.markdown("<h3 class='sub-header'>User Added Successfully!</h3>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class='success-box'>
                    ✅ User added successfully!<br>
                    <strong>ID:</strong> {user_data['user_id']}<br>
                    <strong>Name:</strong> {user_data['user_name']}
                </div>
                """, unsafe_allow_html=True)
                
                # Show JSON output
                st.markdown("<h3 class='sub-header'>User JSON</h3>", unsafe_allow_html=True)
                user_json = {
                    "user_added": True,
                    "user_id": user_data['user_id'],
                    "user_name": user_data['user_name'],
                    "total_users_after_addition": len(system.users)
                }
                display_json(user_json, "New User Result")
                
                # Show updated count
                st.info(f"**Total users now:** {len(system.users)}")
                
                # Add buttons to add another or go back
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👤 Add Another User"):
                        st.session_state.add_user_submitted = False
                        st.session_state.new_user_data = None
                        st.rerun()
                with col2:
                    if st.button("🏠 Go to Dashboard"):
                        st.session_state.add_user_submitted = False
                        st.session_state.new_user_data = None
                        st.info("Please select 'Dashboard' from the sidebar")
            else:
                st.error("Error: No user data found")
    
    elif menu == "Delete Transaction":
        st.markdown("<h1 class='main-header'>🗑️ Delete Transaction</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<h3 class='sub-header'>Search Transaction</h3>", unsafe_allow_html=True)
            search_term = st.text_input("Search transaction by ID or description:", key="search_trans_del")
            
            filtered_transactions = []
            if search_term:
                filtered_transactions = [
                    t for t in system.transactions 
                    if search_term.lower() in t['id'].lower() or search_term.lower() in t['description'].lower()
                ]
            else:
                filtered_transactions = system.transactions[-10:]  # Show last 10 if no search
            
            if filtered_transactions:
                st.write(f"Found {len(filtered_transactions)} transactions")
                for t in filtered_transactions:
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"""
                            <div class='transaction-card'>
                                <strong>ID:</strong> {t['id']}<br>
                                <strong>Amount:</strong> ${t['amount']:.2f}<br>
                                <strong>Description:</strong> {t['description'][:100]}...
                            </div>
                            """, unsafe_allow_html=True)
                        with col_b:
                            if st.button(f"Delete", key=f"del_trans_{t['id']}"):
                                with st.spinner("Deleting transaction..."):
                                    success, deleted_transaction = system.delete_transaction(t['id'])
                                    if success:
                                        st.markdown(f"""
                                        <div class='success-box'>
                                            ✅ Transaction deleted successfully!<br>
                                            <strong>ID:</strong> {deleted_transaction['id']}<br>
                                            <strong>Amount:</strong> ${deleted_transaction['amount']:.2f}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        # Force rerun to update sidebar
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete transaction.")
            else:
                st.warning("No transactions found.")
        
        with col2:
            st.markdown("<h3 class='sub-header'>Delete by ID</h3>", unsafe_allow_html=True)
            transaction_id_to_delete = st.text_input("Enter Transaction ID to delete:", key="trans_id_del")
            confirm = st.checkbox("I confirm I want to delete this transaction")
            
            # Create a unique key for the delete button
            delete_key = f"delete_trans_{transaction_id_to_delete}"
            
            if st.button("🗑️ Delete Transaction", key=delete_key, type="primary", use_container_width=True, disabled=not confirm):
                if transaction_id_to_delete:
                    with st.spinner("Deleting transaction..."):
                        success, deleted_transaction = system.delete_transaction(transaction_id_to_delete)
                        if success:
                            st.markdown(f"""
                            <div class='success-box'>
                                ✅ Transaction deleted successfully!<br>
                                <strong>ID:</strong> {deleted_transaction['id']}<br>
                                <strong>Amount:</strong> ${deleted_transaction['amount']:.2f}<br>
                                <strong>Description:</strong> {deleted_transaction['description'][:50]}...
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show JSON output
                            st.markdown("<h3 class='sub-header'>Deletion JSON</h3>", unsafe_allow_html=True)
                            deletion_json = {
                                "transaction_deleted": True,
                                "deleted_transaction": deleted_transaction,
                                "remaining_transactions": len(system.transactions)
                            }
                            display_json(deletion_json, "Transaction Deletion Result")
                            
                            # Force rerun to update sidebar
                            st.rerun()
                        else:
                            st.markdown("""
                            <div class='error-box'>
                                ❌ Transaction not found!<br>
                                Please check the Transaction ID.
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a Transaction ID")
    
    elif menu == "Delete User":
        st.markdown("<h1 class='main-header'>🗑️ Delete User</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<h3 class='sub-header'>Search User</h3>", unsafe_allow_html=True)
            search_term = st.text_input("Search user by ID or name:", key="search_user_del")
            
            filtered_users = []
            if search_term:
                filtered_users = [
                    u for u in system.users 
                    if search_term.lower() in u['id'].lower() or search_term.lower() in u['name'].lower()
                ]
            else:
                filtered_users = system.users[-10:]  # Show last 10 if no search
            
            if filtered_users:
                st.write(f"Found {len(filtered_users)} users")
                for u in filtered_users:
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"""
                            <div class='transaction-card'>
                                <strong>ID:</strong> {u['id']}<br>
                                <strong>Name:</strong> {u['name']}
                            </div>
                            """, unsafe_allow_html=True)
                        with col_b:
                            if st.button(f"Delete", key=f"del_user_{u['id']}"):
                                with st.spinner("Deleting user..."):
                                    success, deleted_user = system.delete_user(u['id'])
                                    if success:
                                        st.markdown(f"""
                                        <div class='success-box'>
                                            ✅ User deleted successfully!<br>
                                            <strong>ID:</strong> {deleted_user['id']}<br>
                                            <strong>Name:</strong> {deleted_user['name']}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        # Force rerun to update sidebar
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete user.")
            else:
                st.warning("No users found.")
        
        with col2:
            st.markdown("<h3 class='sub-header'>Delete by ID</h3>", unsafe_allow_html=True)
            user_id_to_delete = st.text_input("Enter User ID to delete:", key="user_id_del")
            confirm = st.checkbox("I confirm I want to delete this user")
            
            # Create a unique key for the delete button
            delete_key = f"delete_user_{user_id_to_delete}"
            
            if st.button("🗑️ Delete User", key=delete_key, type="primary", use_container_width=True, disabled=not confirm):
                if user_id_to_delete:
                    with st.spinner("Deleting user..."):
                        success, deleted_user = system.delete_user(user_id_to_delete)
                        if success:
                            st.markdown(f"""
                            <div class='success-box'>
                                ✅ User deleted successfully!<br>
                                <strong>ID:</strong> {deleted_user['id']}<br>
                                <strong>Name:</strong> {deleted_user['name']}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show JSON output
                            st.markdown("<h3 class='sub-header'>Deletion JSON</h3>", unsafe_allow_html=True)
                            deletion_json = {
                                "user_deleted": True,
                                "deleted_user": deleted_user,
                                "remaining_users": len(system.users)
                            }
                            display_json(deletion_json, "User Deletion Result")
                            
                            # Force rerun to update sidebar
                            st.rerun()
                        else:
                            st.markdown("""
                            <div class='error-box'>
                                ❌ User not found!<br>
                                Please check the User ID.
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a User ID")
    
    elif menu == "View Transactions":
        st.markdown("<h1 class='main-header'>📋 All Transactions</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("Search in transactions:", key="search_trans_view")
        
        if search_term:
            filtered_transactions = [t for t in system.transactions if search_term.lower() in t['description'].lower()]
        else:
            filtered_transactions = system.transactions
        
        st.metric("Total Transactions", len(filtered_transactions))
        
        # Show JSON button
        if st.button("📄 Show Transactions in JSON"):
            transactions_json = {
                "total_transactions": len(filtered_transactions),
                "search_term": search_term if search_term else "All",
                "transactions": [
                    {
                        "id": t['id'],
                        "amount": t['amount'],
                        "description": t['description']
                    } for t in filtered_transactions
                ]
            }
            display_json(transactions_json, "All Transactions")
        
        # Pagination
        items_per_page = 20
        total_pages = max(1, (len(filtered_transactions) + items_per_page - 1) // items_per_page)
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key="trans_page")
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(filtered_transactions))
        
        for t in filtered_transactions[start_idx:end_idx]:
            with st.container():
                st.markdown(f"""
                <div class='transaction-card'>
                    <strong>ID:</strong> {t['id']}<br>
                    <strong>Amount:</strong> ${t['amount']:.2f}<br>
                    <strong>Description:</strong> {t['description']}
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "View Users":
        st.markdown("<h1 class='main-header'>👥 All Users</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("Search in users:", key="search_users_view")
        
        if search_term:
            filtered_users = [u for u in system.users if search_term.lower() in u['name'].lower()]
        else:
            filtered_users = system.users
        
        st.metric("Total Users", len(filtered_users))
        
        # Show JSON button
        if st.button("📄 Show Users in JSON"):
            users_json = {
                "total_users": len(filtered_users),
                "search_term": search_term if search_term else "All",
                "users": [
                    {
                        "id": u['id'],
                        "name": u['name']
                    } for u in filtered_users
                ]
            }
            display_json(users_json, "All Users")
        
        col1, col2, col3 = st.columns(3)
        for i, user in enumerate(filtered_users):
            with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
                st.markdown(f"""
                <div style='padding: 0.5rem; background: #F1F5F9; border-radius: 0.5rem; margin: 0.5rem 0;'>
                    <strong>{user['name']}</strong><br>
                    <small>ID: {user['id']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "Statistics":
        st.markdown("<h1 class='main-header'>📈 System Statistics</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Transaction Statistics")
            if system.transactions:
                total_amount = sum(t['amount'] for t in system.transactions)
                avg_amount = total_amount / len(system.transactions)
                min_trans = min(system.transactions, key=lambda x: x['amount'])
                max_trans = max(system.transactions, key=lambda x: x['amount'])
                
                st.metric("Total Amount", f"${total_amount:,.2f}")
                st.metric("Average Transaction", f"${avg_amount:,.2f}")
                st.metric("Smallest Transaction", f"${min_trans['amount']:.2f}")
                st.write(f"ID: {min_trans['id']}")
                st.metric("Largest Transaction", f"${max_trans['amount']:.2f}")
                st.write(f"ID: {max_trans['id']}")
        
        with col2:
            st.markdown("### 👥 User Statistics")
            st.metric("Total Users", len(system.users))
            
            # Count by name length
            name_lengths = [len(u['name'].split()) for u in system.users if u['name']]
            if name_lengths:
                avg_name_parts = sum(name_lengths) / len(name_lengths)
                st.metric("Avg Name Parts", f"{avg_name_parts:.1f}")
        
        # Transaction types
        st.markdown("### 🔤 Transaction Types")
        keyword_counts = defaultdict(int)
        keywords = ['payment', 'salary', 'contract', 'invoice', 'bonus', 'transfer', 'received', 'request']
        
        for t in system.transactions:
            desc_lower = t['description'].lower()
            for keyword in keywords:
                if keyword in desc_lower:
                    keyword_counts[keyword] += 1
                    break
        
        if keyword_counts:
            cols = st.columns(len(keyword_counts))
            for idx, (keyword, count) in enumerate(sorted(keyword_counts.items())):
                with cols[idx]:
                    st.metric(keyword.title(), count)
        
        # Show Statistics in JSON
        if st.button("📊 Show Statistics in JSON"):
            statistics_json = {
                "transaction_statistics": {
                    "total_transactions": len(system.transactions),
                    "total_amount": total_amount,
                    "average_transaction": avg_amount,
                    "smallest_transaction": {
                        "id": min_trans['id'],
                        "amount": min_trans['amount']
                    },
                    "largest_transaction": {
                        "id": max_trans['id'],
                        "amount": max_trans['amount']
                    }
                },
                "user_statistics": {
                    "total_users": len(system.users),
                    "average_name_parts": avg_name_parts if name_lengths else 0
                },
                "transaction_types": keyword_counts
            }
            display_json(statistics_json, "System Statistics")
    
    elif menu == "Demo":
        st.markdown("<h1 class='main-header'>🎬 Demo Mode</h1>", unsafe_allow_html=True)
        
        if st.button("Run Demo"):
            with st.spinner("Running demo..."):
                
                demo_results = {}
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Test 1: Exact Match")
                    matches, extracted_name, _ = system.find_user_matches_for_transaction("caqjJtrI")
                    if matches:
                        st.success(f"✅ Found {len(matches)} matches")
                        st.write(f"Best match: **{matches[0]['name']}**")
                        st.write(f"Match score: {matches[0]['match_metric']:.3f}")
                        demo_results["exact_match"] = {
                            "found": True,
                            "matches_count": len(matches),
                            "best_match": matches[0]['name'],
                            "best_score": matches[0]['match_metric']
                        }
                    else:
                        demo_results["exact_match"] = {"found": False}
                
                with col2:
                    st.markdown("### Test 2: Similar Transactions")
                    results, _ = system.find_similar_transactions("From Liam Johnson", 0.1, 3)
                    st.success(f"✅ Found {len(results)} similar transactions")
                    if results:
                        st.write(f"First result: **{results[0]['id']}**")
                        demo_results["similar_transactions"] = {
                            "found": True,
                            "results_count": len(results),
                            "first_result_id": results[0]['id']
                        }
                    else:
                        demo_results["similar_transactions"] = {"found": False}
                
                st.markdown("### Test 3: Fuzzy Matching")
                test_desc = "From Liam J. Johnson for Deel"
                matches, extracted_name, _ = system.find_user_matches_for_transaction(test_desc)
                st.write(f"Query: `{test_desc}`")
                st.write(f"Extracted: **{extracted_name}**")
                if matches:
                    st.success(f"✅ Found {len(matches)} matches")
                    demo_results["fuzzy_matching"] = {
                        "found": True,
                        "matches_count": len(matches),
                        "extracted_name": extracted_name
                    }
                else:
                    demo_results["fuzzy_matching"] = {"found": False}
                
                st.markdown("<div class='success-box'>✅ Demo completed successfully!</div>", unsafe_allow_html=True)
                
                # Show Demo Results in JSON
                st.markdown("<h3 class='sub-header'>Demo Results JSON</h3>", unsafe_allow_html=True)
                display_json(demo_results, "Demo Results")

if __name__ == "__main__":
    main()
