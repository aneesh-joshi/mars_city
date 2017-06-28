from __future__ import absolute_import, division, print_function
from threading import Thread
import sys
import os
import time
sys.path.insert(0, '../hexoskin_helper')
sys.path.insert(0, '../anomaly_detector')
import utility_helper as util
import resource_helper as resource
import anomaly_detector as ad
import vt_helper as vth
import ConfigParser


__author__ = 'abhijith'


def atrial_fibrillation_helper(auth):
    '''
    Returns the rr_interval data in realtime.
            @param auth:		Authentication token
    '''
    recordID = resource.get_active_record_list(auth)[0]
    if recordID not in resource.get_active_record_list(auth):
        # record not updated in realtime.
        return -1

    AD = ad.AnomalyDetector()

    config = ConfigParser.RawConfigParser()
    dirname = os.path.dirname(os.path.realpath(__file__))
    cfg_filename = os.path.join(dirname,
                                '../anomaly_detector/anomaly_detector.cfg')
    config.read(cfg_filename)

    window_size = config.getint('Atrial Fibrillation', 'window_size')

    datatypes = [util.datatypes['rrinterval'][0],
                 util.datatypes['hr_quality'][0]]
    resource.AF_realtime(auth, recordID, AD.af_anomaly_detect,
                         window_size, datatypes)
    # Successfully finished. Astronaut docked.
    return 1


def ventricular_tachycardia_helper(auth):
    '''
    Returns the rr_interval data in realtime.
            @param auth:		Authentication token
    '''
    recordID = resource.get_active_record_list(auth)[0]
    if recordID not in resource.get_active_record_list(auth):
        # record not updated in realtime.
        return -1

    VTBD = vth.VTBeatDetector()

    datatypes = [util.raw_datatypes['ecg'][0],
                 util.datatypes['rrinterval'][0],
                 util.datatypes['rrintervalstatus'][0],
                 util.datatypes['heartrate'][0],
                 util.datatypes['hr_quality'][0]]

    # Call to get data
    th1 = Thread(target=resource.VT_realtime, args=[
                 auth, recordID, VTBD, datatypes])
    th1.start()
    # resource.VT_realtime(auth, recordID, VTBD, datatypes)

    # Call to add anomaly into the data base
    th2 = Thread(target=VTBD.ping_AD_dict)
    th2.start()
    # VTBD.ping_AD_dict()

    # Call to keep VT datastructure size under limit
    time.sleep(120)
    while(True):
        VTBD.delete_data()
        time.sleep(2)

    # Successfully finished. Astronaut docked.
    return 1


def main(argv):
    auth = util.auth_login()
    # af = Thread(target=atrial_fibrillation_helper, args=[auth])
    # af.start()
    # vt = Thread(target=ventricular_tachycardia_helper, args=[auth])
    # vt.start()
    if argv[1] == 'af':
        atrial_fibrillation_helper(auth)
    elif argv[1] == 'vt':
        ventricular_tachycardia_helper(auth)


if __name__ == "__main__":
    main(sys.argv)
