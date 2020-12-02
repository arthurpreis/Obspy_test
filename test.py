
import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt

import obspy
import obspy.clients.fdsn.client
Client = obspy.clients.fdsn.client.Client
client = Client("IRIS")

import numpy as np
import datetime

from gwpy.plot import Plot

import gwpy.time
import gwpy.timeseries

import astropy.time
from astropy import units


def get_timeseries(client, channel, start_time, end_time):
    '''

    :param client:
    :param channel:
    :param start_time: in UTC
    :param end_time: in UTC
    :param sample_rate: float
    :param calibration:
    :return: the data (hopefully)
    '''

    # start_time = obspy.UTCDateTime(start_time[0], start_time[1], start_time[2], start_time[3],
    #                                start_time[4],start_time[5], start_time[6])
    # end_time = obspy.UTCDateTime(end_time[0], end_time[1], end_time[2], end_time[3],
    #                                end_time[4], end_time[5], end_time[6])
    #
    # start_datetime = datetime.datetime(start_time[0], start_time[1], start_time[2], start_time[3],
    #                                start_time[4],start_time[5], start_time[6])

    start_datetime = datetime.datetime(2019, 11, 20, 2)
    start_gps = gwpy.time.to_gps(start_datetime)


    channelSplit = channel.split(":")
    net = channelSplit[0]
    stat = channelSplit[1]
    chan = channelSplit[3]

    inventory = client.get_stations(starttime=start_time, endtime=end_time, station=stat, network=net, channel=chan,
                                    location='*', level='response')

    response = inventory.get_response(channel.replace(':', '.'), start)
    #calibration = response.instrument_sensitivity.value
    sample_rate = inventory[0].stations[0].channels[0].sample_rate

    st = client.get_waveforms(net, stat, channelSplit[2], chan, start_time, end_time)

    data = np.array(st[0].data)
    data = data.astype(float)
    #data = data / calibration
    data = data - np.median(data)

    dataFull = gwpy.timeseries.TimeSeries(data, epoch=start_gps, channel=net, name=stat,
                                          sample_rate=float(sample_rate))

    cutoff_low = 0.1
    dataFull = dataFull.lowpass(frequency=cutoff_low)

    return dataFull

# start = [2019, 11, 20, 2, 0, 0, 0]
# end = [2019, 11, 20, 16, 0, 0, 0]

start = obspy.UTCDateTime(2019, 11, 20, 2, 0, 0, 0)
end = obspy.UTCDateTime(2019, 11, 20, 16, 0, 0, 0)

channel = 'IU:KIP:10:VMV'

your_data = get_timeseries(client, channel=channel, start_time=start, end_time=end)

title_of_plot = 'KIP Data 11_20_2019'
plot = Plot(your_data, ylabel='m/s', title=title_of_plot) #yscale='log',

name_of_plot = 'kip_test_11_20_2019_titles_v7'
# test_11_20_2019:
# https://ldas-jobs.ligo-wa.caltech.edu/~detchar/summary/day/20191120/sei/ground_blrms_overview/

plt.savefig("{}.png".format(name_of_plot))
