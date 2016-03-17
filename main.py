mport argparse
import satellite
import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import glob
import os.path

def construct_site_list(not_in_list):

    all_sites = ['ASCAT', 'OTROSAT','OTROSAT2']
    sites = list(set(all_sites) - set(not_in_list))
    return sites

def plot_data_matrix(data_matrix):
    pass


# Clean working environment (should be called before main)
def clean():
    import os
    os.system("rm -f /tmp/*.gz /tmp/*.nc")

def main():

	#define parser data
    parser = argparse.ArgumentParser(description='Plotting satellite data.')
    #first arguments. Dates. TODO:SPECIFY INITIAL AND FINAL ORDER
    parser.add_argument('date', metavar='date_time_YYYY.MM.DD', type=str, nargs=2,\
		      help='time interval')
    #specify sattelites to exclude from command line. TODO: change to flag!
    parser.add_argument('satellite', metavar='SATELLITE_NAME', type=str, nargs='?',\
		      help='satellite name')

    args=parser.parse_args()
    initialDate = args.date[0]
    finalDate = args.date[1]

    #construct list of satellites to exclude
    if not args.satellite:
        not_in_list = []
    else:
        not_in_list = args.satellite.split('+')

    #construct definite list
    sites = construct_site_list(not_in_list)

    #ASCAT implementation.
    ascat = satellite.ASCAT(initialDate, finalDate)
    ascat.convert_to_datetime()
    ascat.download_files()

    # Figure
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=0,urcrnrlon=360,lat_ts=20,resolution='c')

    # Color bar
    #
    cmap = plt.cm.jet
    cmap.set_under((0,0,0,0))

    for src_name in glob.glob(os.path.join("/tmp", '*.nc')):
        base = os.path.basename(src_name)
        ascat.plot_data(src_name, m,cmap)

    plt.title('Sfc Wind Speed') #agregar fecha y dato del satelite

    plt.show()
    #future implementation for several satellites
    #for site in sites:
    #    pass
        #a_satellite = satellite.Satellite(args.satellite[0],initialDate, finalDate)

if __name__ == "__main__":
    clean()
    main()

