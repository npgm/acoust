#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Acoust In
# Generated: Thu Dec 11 18:44:03 2014
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

class acoust_in(gr.top_block):

    def __init__(self, port=8000, payload=32, carrier=20000):
        gr.top_block.__init__(self, "Acoust In")

        ##################################################
        # Variables
        ##################################################
        self.transistion = transistion = 100
        self.sps = sps = 2
        self.sideband_rx = sideband_rx = 1000
        self.sideband = sideband = 1000
        self.samp_rate = samp_rate = 48000
        self.port = port = port
        self.payload = payload
        self.interpolation = interpolation = 200
        self.carrier = carrier

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=interpolation,
                taps=None,
                fractional_bw=None,
        )
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, (filter.firdes.low_pass(1, samp_rate, sideband_rx,100)), carrier, samp_rate)
        self.digital_gfsk_demod_0 = digital.gfsk_demod(
        	samples_per_symbol=sps,
        	sensitivity=1.0,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, "", port, payload, True)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code="",
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )
        self.audio_source_0 = audio.source(48000, "", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.digital_gfsk_demod_0, 0))
        self.connect((self.digital_gfsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_udp_sink_0, 0))



    def get_transistion(self):
        return self.transistion

    def set_transistion(self, transistion):
        self.transistion = transistion

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_sideband_rx(self):
        return self.sideband_rx

    def set_sideband_rx(self, sideband_rx):
        self.sideband_rx = sideband_rx
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((filter.firdes.low_pass(1, self.samp_rate, self.sideband_rx,100)))

    def get_sideband(self):
        return self.sideband

    def set_sideband(self, sideband):
        self.sideband = sideband

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((filter.firdes.low_pass(1, self.samp_rate, self.sideband_rx,100)))

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation

    def get_carrier(self):
        return self.carrier

    def set_carrier(self, carrier):
        self.carrier = carrier
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.carrier)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = acoust_in()
    tb.start()
    tb.wait()
