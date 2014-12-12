#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Acoust Out
# Generated: Wed Nov  5 02:56:48 2014
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser

class acoust_out(gr.top_block):

    def __init__(self, setfd, setcar):
        gr.top_block.__init__(self, "Acoust Out")

        ##################################################
        # Variables
        ##################################################
        self.transistion = transistion = 100
        self.sps = sps = 2
        self.sideband_rx = sideband_rx = 1000
        self.sideband = sideband = 1000
        self.samp_rate = samp_rate = 48000
        self.payload = payload =4 
        self.interpolation = interpolation = 200
        self.fd = fd = setfd
        self.carrier = carrier = setcar

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interpolation,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes.band_pass (0.50,samp_rate,carrier-sideband,carrier+sideband,transistion)), -carrier, samp_rate)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
        	samples_per_symbol=sps,
        	sensitivity=1.0,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, fd, False)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=sps,
        		bits_per_symbol=1,
        		preamble="",
        		access_code="",
        		pad_for_usrp=False,
        	),
        	payload_length=payload,
        )
        self.audio_sink_0 = audio.sink(48000, "", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))


# QT sink close method reimplementation

    def get_transistion(self):
        return self.transistion

    def set_transistion(self, transistion):
        self.transistion = transistion
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.band_pass (0.50,self.samp_rate,self.carrier-self.sideband,self.carrier+self.sideband,self.transistion)))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_sideband_rx(self):
        return self.sideband_rx

    def set_sideband_rx(self, sideband_rx):
        self.sideband_rx = sideband_rx

    def get_sideband(self):
        return self.sideband

    def set_sideband(self, sideband):
        self.sideband = sideband
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.band_pass (0.50,self.samp_rate,self.carrier-self.sideband,self.carrier+self.sideband,self.transistion)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.band_pass (0.50,self.samp_rate,self.carrier-self.sideband,self.carrier+self.sideband,self.transistion)))

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation

    def get_fd(self):
        return self.fd

    def set_fd(self, fd):
        self.fd = fd

    def get_carrier(self):
        return self.carrier

    def set_carrier(self, carrier):
        self.carrier = carrier
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.band_pass (0.50,self.samp_rate,self.carrier-self.sideband,self.carrier+self.sideband,self.transistion)))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-self.carrier)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = acoust_out()
    tb.start()
    tb.wait()

