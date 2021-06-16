import random

def get_user_agent():
    return random.choice(user_agent)

def no_of_agents():
    return len(user_agent)

def get_stocks(stock):
    return stocks[stock]

_inmerger = ["CFL", "HFL", "HATH", "SYFL", "NIB", "HBL", "JBNL"]
stocks = {
    "mystocks":["CHCL", "NIFRA", "ccbl", "GBIME", "GBLBS", "GLH", "NICL", "NICLBSL", "PLI", "SRBL", "CHDC", "CGH" ],
    "birajstocks":[ "UPPER", "RHPL", "PLI", "JLI", "SHL", "API"],
    "dadstocks": ["SBI", "RHPL", "NLICL"],
    "banking" : [
        "ADBL","BOKL", "CCBL", "CZBIL", "CBL", "EBL",
        "GBIME", "KBL", "LBL", 
        "MBL", "MEGA", "NABIL", "NBB", "NBL",
        "NCCB", "SBI", "NICA", "NMB", "PRVU", 
        "PCBL", "SANIMA", "SBL", "SCB", "SRBL"
    ],

    "finance" : [
        "BFC","CMB","CFCL","GFCL","GMFIL", "GUFL",
        "ICFC", "JFL", "LFC", "MFIL", "MPFL",
        "NFS", "NSM", "PFL", "PROFL", "RLFL", "SFC", "SFCL", 
        "SIFC", "SFFIL", 
        "UFL" 
    ],

    "hotels" : ["TRH","YHL"],

    "manufacture" : [
        "AVU", "BSL", "BNL", "BNT", "BSM", "FHL", "GRU", "HBT",
        "HDL", "JSM", "NBBU", "NKU", "NLO", "NVG", "RJM", "SHIVM",
        "SBPP", "SRS", "UNL"
    ],
    "others" : ["NTC","NFD", "NIFRA", "NRIC"],

    "hydropower" : [
        "AKJCL","API", "AKPL", "AHPC", "BARUN", "BPCL",
        "CHL","CHCL", "DHPL", "GHL", "GLH", "HDHPC", "HURJA",
        "HPPL","JOSHI", "KPCL", "KKHC", "LEC", "MEN", "MHNL",
        "NHPC","NHDL", "NGPL", "PMHPL", "PPCL", "RADHI", "RRHP",
        "RHPL","RHPC", "RURU", "SHPC", "SJCL", "SSHL", "CHDC",
        "SHEL","SPDL", "UNHPL", "UMRH", "UMHL", "UPCL", "UPPER",
    ],
    "trading" : ["BBC", "NTL", "NWC", "STC"],

    "nonlifeinsu" : ["AIL", "EIC", "GIC", "HGI", "IGI",
        "LGIL", "NIL", "NICL", "NLG", "PRIN",
        "PIC", "PICL", "RBCL", "SIC",
        "SGI", "SICL", "SIL", "UIC",
    ],
    "devbank" : [
        "BHBL", "EDBL", "CORBL","GDBL", "GBBL",
        "GRDBL", "HAMRO", "JBBL", "KSBBL", "KNBL",
        "KRBL", "LBBL", "MLBL", "MDB", "MNBBL",
        "NABBC", "NIDC", "ODBL", "SHBL", "SBBLJ",
        "SAPDBL", "SADBL", "SHINE", "SINDU", "TMDBL",
    ],
    "microfinance":[
        "ACLBSL", "AKBSL", "AMFI", "ALBSL", "CBBL",
        "CLBSL", "DDBL", "FMDBL", "FOWAD", "GMFBS", "GGBSL",
        "GILB", "GBLBS", "GLBSL", "ILBS", "JSLBB", "KMCDB",
        "KLBSL", "LLBS", "MLBSL", "MSMBS", "MSLB", "MERO",
        "MMFDB", "MLBBL", "NADEP", "NMFBS", "NAGRO", "NSEWA",
        "NLBBL", "NICLBSL", "NUBL", "NMBMF", "RMDC", "RSDC",
        "SABSL", "SDLBSL", "SMATA", "SLBSL", "SKBBL", "SNLB",
        "SPARS", "SMFDB", "SMB", "SLBS", "SWBBL",
        "SMFBS", "SDESI", "SLBBL", "USLB", "VLBS", "WOMI",
    ],
    "lifeinsu" : [
        "ALICL", "GLICL", "JLI", "LICN", "NLICL",
        "NLIC", "PLI", "PLIC", "RLI", "SLICL",
    ]
}

user_agent=[ 
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/73.0",
    "Mozilla/5.0 (X11; OpenBSD i386; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20191022 Firefox/70.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20190101 Firefox/70.0",
    "Mozilla/5.0 (Windows; U; Windows NT 9.1; en-US; rv:12.9.1.11) Gecko/20100821 Firefox/70",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:69.2.1) Gecko/20100101 Firefox/69.2",
    "Mozilla/5.0 (Windows NT 6.1; rv:68.7) Gecko/20100101 Firefox/68.7",
    "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.13; ko; rv:1.9.1b2) Gecko/20081201 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows NT 5.0; Windows NT 5.1; Windows NT 6.0; Windows NT 6.1; Linux; es-VE; rv:52.9.0) Gecko/20100101 Firefox/52.9.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.59.12) Gecko/20160044 Firefox/52.59.12",
    "Mozilla/5.0 (X11; Ubuntu i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (X11;  Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a1) Gecko/20060814 Firefox/51.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20120121 Firefox/46.0",
]

