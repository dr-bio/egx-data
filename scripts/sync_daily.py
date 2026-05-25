
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import os
import time

tv = TvDatafeed()

TICKERS = [
    "AALR","ABUK","ACAMD","ACAP","ACGC","ACTF","ADCI","ADIB","ADPC","ADRI",
    "AFDI","AFMC","AIFI","AIH","AJWA","ALCN","ALEX","ALUM","AMER","AMES",
    "AMIA","AMOC","AMPI","ARAB","ARCC","AREH","ARVA","ASCM","ASPI","ATLC",
    "ATQA","AXPH","BIDI","BIGP","BINV","BIOC","BONY","BTFH","CAED","CANA",
    "CCAP","CCRS","CEFM","CERA","CICH","CIEB","CIRA","CLHO","CNFN","COMI",
    "COPR","COSG","CPCI","CRST","CSAG","DAPH","DEIN","DGTZ","DOMT","DSCW",
    "DTPP","EALR","EASB","EAST","EBSC","ECAP","EDFM","EEII","EFIC","EFID",
    "EFIH","EGAL","EGAS","EGBE","EGCH","EGSA","EGTS","EHDR","EITP","ELEC",
    "ELKA","ELNA","ELSH","ELWA","EMFD","ENGC","EOSB","EPCO","EPPK","ETEL",
    "ETRS","EXPA","FAIT","FCMD","FIRE","FNAR","FWRY","GBCO","GDWA","GGCC",
    "GGRN","GIHD","GMCI","GPIM","GRCA","GSSC","GTHE","GTWL","HDBK","HELI",
    "HRHO","IBCT","ICFC","ICID","IDRE","IEEC","IFAP","INEG","INFI","IRAX",
    "IRON","ISMA","ISMQ","ISPH","JUFO","KABO","KWIN","KZPC","LCSW","LKGP",
    "MAAL","MASR","MBEG","MCQE","MCRO","MENA","MEPA","MFPC","MFSC","MHOT",
    "MICH","MILS","MKIT","MOIL","MOIN","MPCI","MPCO","MPRC","MTIE","MAAL",
    "NARE","NBKE","NCCW","NDRL","NEDA","NHPS","NINH","NCCW","OBRI","OCDI",
    "OCPH","ODIN","OFH","OIH","OLFI","ORAS","ORHD","ORWE","PACH","PHAR",
    "PHDC","PHTV","POUL","PRCL","PRDC","PRMH","QNBE","RACC","RAKT","RAYA",
    "RMDA","ROTO","RREI","RTVC","SAIB","SAUD","SCEM","SCFM","SDTI","SEIG",
    "SIPC","SKPC","SMFR","SNFC","SPIN","SPMD","SUGR","SVCE","SWDY","TALM",
    "TAQA","TMGH","TYCN","UBEE","UEFM","UEGC","UNIP","UNIT","UPMS","UTOP",
    "VALU","VERT","VLMR","WCDF","WKOL","ZEOT","AMOC","ISMQ","ISPH","JUFO",
    "KABO","KWIN","KZPC","LCSW","LKGP","MASR","MBEG","MCQE","MEGM","MENA",
    "MFSC","MHOT","MICH","MILS","MKIT","MOIL","MOIN","MPCI","NARE","RREI",
    "TANM","ZMID",
]

TICKERS = list(dict.fromkeys(TICKERS))
os.makedirs("data/ohlcv", exist_ok=True)

success = 0
failed = []

for ticker in TICKERS:
    try:
        df = tv.get_hist(
            symbol=ticker,
            exchange='EGX',
            interval=Interval.in_daily,
            n_bars=1000
        )
        if df is not None and len(df) >= 100:
            df = df.reset_index()
            df.columns = ['date','symbol','open','high','low','close','volume']
            df['symbol'] = ticker
            df.to_csv(f"data/ohlcv/{ticker}.csv", index=False)
            success += 1
            print(f"✅ {ticker}: {len(df)} rows")
        else:
            failed.append(ticker)
            print(f"❌ {ticker}: no data")
    except Exception as e:
        failed.append(ticker)
        print(f"⚠️ {ticker}: {e}")
    time.sleep(0.5)

print(f"\n✅ Success: {success}")
print(f"❌ Failed: {failed}")

summary = pd.DataFrame({
    'date': [pd.Timestamp.now().date()],
    'success': [success],
    'failed': [len(failed)],
    'failed_list': [','.join(failed)]
})
summary.to_csv("data/sync_log.csv", index=False)
