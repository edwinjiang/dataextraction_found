#!/usr/bin/python
#encoding:utf8

from bs4 import BeautifulSoup
import os
import pprint
import re
import argparse
import json
import csv

DATADIR = ""
DATAFILE = ""

def extract_data(**kwargs):


    awrfile = os.path.join(DATADIR, kwargs["file"])

    #Get DB Name
    with open(awrfile) as f:
        soup = BeautifulSoup(f, 'lxml')

        # DB Name
        dbname = []

        for rawdata in soup.find_all('table'):
            if re.compile('Database Summary').search(rawdata['summary']):
                trdatas = rawdata.find_all(name='tr')
                for trdata in trdatas:
                    tddatas = BeautifulSoup(str(trdata), "html.parser")
                    for tddata in tddatas.find_all(name='td'):
                        if tddata.get('headers') != None:
                            if re.compile('UniqueName').search(tddata.get('headers')[1]):
                                dbname.append({"DB Name":tddata.string})
        #print dbname[0]["DB Name"]
        f.close()

    # IOPS Metircs
    with open(awrfile) as f:
        soup = BeautifulSoup(f,'lxml')

        io_data = []
        result = {}
        total_iops = 0
        total_throughput = 0

        pattern_io =  re.compile('physical')
        pattern_io_iops_metric = re.compile('total IO requests')
        # Throughput metric
        pattern_io_throughput_metric = re.compile('total bytes')


        for rawdata in soup.find_all('table'):
            if re.compile('System Statistics').search(rawdata['summary']):
                trdatas =  rawdata.find_all(name='tr')
                for trdata in trdatas:
                    tddatas = BeautifulSoup(str(trdata), "html.parser")
                    tddata = tddatas.find_all(name='td')
                    try:
                        if  (pattern_io.match(tddata[0].string)):
                            io_data.append({'name':tddata[0].string,'total':float(tddata[1].string.replace(',','')),'per second':float(tddata[2].string.replace(',','')),'per trans':float(tddata[3].string.replace(',',''))})
                    except Exception,e:
                         pass
        #print data
        for i in range(len(io_data)):
            if pattern_io_iops_metric.search(io_data[i]["name"]):
                total_iops += io_data[i]["per second"]
                result[io_data[i]["name"]] = io_data[i]["per second"]
            if pattern_io_throughput_metric.search(io_data[i]["name"]):
                total_throughput += io_data[i]["per second"]
                result[io_data[i]["name"]] = io_data[i]["per second"]
        result["Total IOPS"] = total_iops
        result["Total ThroughPut"] = total_throughput
        json_io = json.dumps(result)
        #print result
        #pprint.pprint(json_io)
        #print result["physical write total IO requests"]
        f.close()

        # CPU NMtrics
        with open(awrfile) as f:
            soup = BeautifulSoup(f, 'lxml')
            #CPU metric
            pattern_cpu_Busy = re.compile('%Busy')
            pattern_cpu_Usr = re.compile('%Usr')
            pattern_cpu_Sys = re.compile('%Sys')
            cpu_data = []
            instance = 0
            for rawdata in soup.find_all('table'):
                if re.compile('OS Statistics By Instance').search(rawdata['summary']):
                    trdatas = rawdata.find_all(name='tr')
                    for trdata in trdatas:
                        tddatas = BeautifulSoup(str(trdata), "html.parser")
                        for tddata in  tddatas.find_all(name='td'):
                            #print tddata
                            if tddata.get('scope') != None:
                                if re.compile('row').search(tddata.get('scope')):
                                    instance=tddata.string
                            # if tddata.get('headers') != None:
                            #     if pattern_cpu_Busy.search(tddata.get('headers')[1]):
                            #         cpu_data["Instance#"]=instance
                            #         cpu_data["%Busy"]=tddata.string
                            #     if pattern_cpu_Usr.search(tddata.get('headers')[1]):
                            #         cpu_data["Instance#"]=instance
                            #         cpu_data["%Usr"]=tddata.string
                            #     if pattern_cpu_Sys.search(tddata.get('headers')[1]):
                            #         cpu_data["Instance#"]=instance
                            #         cpu_data["%Sys"]=tddata.string

                            if tddata.get('headers') != None:
                                if pattern_cpu_Busy.search(tddata.get('headers')[1]):
                                    cpu_data.append({'Instance#':instance,'%Busy':tddata.string})
                                if pattern_cpu_Usr.search(tddata.get('headers')[1]):
                                    cpu_data.append({'Instance#': instance,'%Usr': tddata.string})
                                if pattern_cpu_Sys.search(tddata.get('headers')[1]):
                                    cpu_data.append({'Instance#': instance,'%Sys': tddata.string})
        # cpudata =[]
        # for i in range(len(cpu_data)):
        #     for key,value in cpu_data[i].items():
        #         print key,value
        f.close()

        #Foregroud Wait Time Metrics
        with open(awrfile) as f:
            soup = BeautifulSoup(f, 'lxml')

            #IO latency calculation
            db_file_parallel_read = re.compile('db file parallel read')
            db_file_sequential_read = re.compile('db file sequential read')
            control_file_sequential_read = re.compile('control file sequential read')
            foregroud_waittime ={}


            for rawdata in soup.find_all('table'):
                if re.compile('This table displays foreground wait event information').search(rawdata['summary']):
                    trdatas = rawdata.find_all(name='tr')
                    for trdata in trdatas:
                        tddatas = BeautifulSoup(str(trdata), "html.parser")
                        tddata=tddatas.find_all(name='td')
                        try:
                            if (db_file_parallel_read.match(tddata[1].string)):
                                foregroud_waittime["db file parallel read Avg Wait time"]=tddata[5].string
                                foregroud_waittime["db file parallel read Waits"]=tddata[2].string
                            if (db_file_sequential_read.match(tddata[1].string)):
                                foregroud_waittime["db file sequential read Avg Wait time"]=tddata[5].string
                                foregroud_waittime["db file sequential read Waits"]=tddata[2].string
                            if (control_file_sequential_read.match(tddata[1].string)):
                                foregroud_waittime["control file sequential read Avg Wait time"]=tddata[5].string
                                foregroud_waittime["control file sequential read write Waits"]=tddata[2].string
                        except Exception, e:
                            pass
            #print foregroud_waittime
            f.close()

            # Backgroud Wait Time Metrics
            with open(awrfile) as f:
                soup = BeautifulSoup(f, 'lxml')

                # IO latency calculation
                log_file_parallel_write = re.compile('log file parallel write')
                control_file_parallel_write = re.compile('control file parallel write')
                backgroud_waittime = {}

                for rawdata in soup.find_all('table'):
                    if re.compile('This table displays background wait event information').search(rawdata['summary']):
                        trdatas = rawdata.find_all(name='tr')
                        for trdata in trdatas:
                            tddatas = BeautifulSoup(str(trdata), "html.parser")
                            tddata = tddatas.find_all(name='td')
                            try:
                                if (log_file_parallel_write.match(tddata[1].string)):
                                    backgroud_waittime["log file parallel write Avg Wait time"]=tddata[5].string
                                    backgroud_waittime["log file parallel write Waits"]=tddata[2].string
                                if (control_file_parallel_write.match(tddata[1].string)):
                                    backgroud_waittime["control file parallel write Avg Wait time"]=tddata[5].string
                                    backgroud_waittime["control file parallel write write Waits"]=tddata[2].string
                            except Exception, e:
                                pass
                #print backgroud_waittime
                f.close()

    csvfile=file(dbname[0]["DB Name"]+".csv",'ab+')
    csvfile.truncate()
    writer = csv.writer(csvfile,dialect='excel')
    writer.writerow(['IO Metric'])
    writer.writerow(['physical write total IO requests','physical read total IO requests'])
    writer.writerow([float(result["physical write total IO requests"]), float(result["physical read total IO requests"])])

    writer.writerow(['physical write total bytes', 'physical read total bytes'])
    writer.writerow([float(result["physical write total bytes"]), float(result["physical read total bytes"])])

    writer.writerow('\n')

    writer.writerow(['IO latency'])
    writer.writerow(['IO Wait Event','Avg Wait Time','Waits'])
    writer.writerow(['db file parallel read',foregroud_waittime["db file parallel read Avg Wait time"], foregroud_waittime["db file parallel read Waits"]])
    writer.writerow(['db file sequential read', foregroud_waittime["db file sequential read Avg Wait time"],
                     foregroud_waittime["db file sequential read Waits"]])
    writer.writerow(['control file sequential read', foregroud_waittime["control file sequential read Avg Wait time"],
                     foregroud_waittime["control file sequential read write Waits"]])
    writer.writerow(['log file parallel write', backgroud_waittime["log file parallel write Avg Wait time"],
                     backgroud_waittime["log file parallel write Waits"]])
    writer.writerow(['control file parallel write', backgroud_waittime["control file parallel write Avg Wait time"],
                     backgroud_waittime["control file parallel write write Waits"]])

    writer.writerow('\n')
    writer.writerow(['CPU utilization'])

    for i in range(len(cpu_data)):
        for key, value in cpu_data[i].items():
            writer.writerow([key,value])
    csvfile.close()

def _argparser():
    parser = argparse.ArgumentParser(description='AWR Data Analyze')
    parser.add_argument('-f','--file', action='store', dest='file', required=True, help='AWR File Name')

    return parser.parse_args()

if __name__ == "__main__":
    parser = _argparser()
    conn_args = dict(file=parser.file)
    extract_data(**conn_args)

