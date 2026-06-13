import argparse
import os
import sys
import numpy as np


def main(args):
    url_pattern = "https://ds.nccs.nasa.gov/thredds2/ncss/AMES/NEX/GDDP-CMIP6/{gcm}/{scenario}/{case}/{var}/{var}_day_{gcm}_{scenario}_{case}_gn_{year}.nc?var={var}&north={north}&west={west}&east={east}&south={south}&disableProjSubset=on&horizStride=1&time_start={year}-01-01T12%3A00%3A00Z&time_end={year}-12-31T12%3A00%3A00Z&timeStride=1"
    urls = []
    for gcm in gcms:
        if gcm in [
            "CNRM-CM6-1",
            "CNRM-ESM2-1",
            "GISS-E2-1-G",
            "MIROC-ES2L",
            "UKESM1-0-LL",
        ]:
            case = cases[1]
        elif gcm in ["HadGEM3-GC31-MM", "HadGEM3-GC31-LL"]:
            case = cases[-1]
        else:
            case = cases[0]
        for sce in scenarios[:-1]:
            if gcm == "HadGEM3-GC31-MM" and sce == "ssp245":
                continue
            for year in np.arange(future_year_range[0], future_year_range[1] + 1):
                for var in vars_type:
                    if gcm in ["BCC-CSM2-MR", "NESM3"] and var == "hurs":
                        continue
                    if gcm in ["IPSL-CM6A-LR", "MIROC6", "NESM3"] and var == "huss":
                        continue
                    if gcm in ["CESM2", "CESM2-WACCM", "IITM-ESM"] and var in [
                        "tasmax",
                        "tasmin",
                    ]:
                        continue
                    url = url_pattern.format(
                        gcm=gcm,
                        scenario=sce,
                        case=case,
                        year=year,
                        var=var,
                        north=51,
                        west=234,
                        east=294,
                        south=23,
                    )
                    urls.append(url)
    print(len(urls))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download NEX-GDDP-CMIP6 data")
    parser.add_argument(
        "--data_dir",
        dest="data_dir",
        help="Where we download the data",
        default="NEX-GDDP-CMIP6",
        type=str,
    )
    the_args = parser.parse_args()
    main(the_args)
