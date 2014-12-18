#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: GFSK Modem
# Generated: Sun Dec 14 15:16:18 2014
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import mac
import pmt

class gfsk_radio(gr.hier_block2):

    def __init__(self, rate=1e6, access_code_threshold=0, samps_per_sym=2, ampl=1):
        gr.hier_block2.__init__(
            self, "GFSK Modem",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.rate = rate
        self.access_code_threshold = access_code_threshold
        self.samps_per_sym = samps_per_sym
        self.ampl = ampl

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = rate

        ##################################################
        # Message Queues
        ##################################################
        mac_packet_deframer_0_msgq_out = mac_packet_to_pdu_0_msgq_in = gr.msg_queue(2)

        ##################################################
        # Blocks
        ##################################################
        self.pad_source_1 = None;self.message_port_register_hier_out("msg_in")
        self.pad_sink_0_0 = None;self.message_port_register_hier_in("msg_out")
        self.mac_packet_to_pdu_0 = mac.packet_to_pdu(msgq=mac_packet_to_pdu_0_msgq_in, dewhiten=True, output_invalid=False)
        self.mac_packet_framer_0 = mac.packet_framer(
            access_code="",
        	whitener_offset=0,
        	rotate_whitener_offset=0,
        	whiten=True,
        	preamble=''.join(['\x55']*((256*1)/8/samps_per_sym)),
        	postamble=''.join(['\x00']*(16/8/samps_per_sym)*0),
        )
        self.mac_packet_deframer_0 = mac.packet_deframer(msgq=mac_packet_deframer_0_msgq_out, access_code="", threshold=access_code_threshold)
        self.mac_burst_tagger_0 = mac.burst_tagger('length', samps_per_sym*8, 32*0+ 0, 16*0 + 16)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
        	samples_per_symbol=samps_per_sym,
        	sensitivity=1.0,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.digital_gfsk_demod_0 = digital.gfsk_demod(
        	samples_per_symbol=samps_per_sym,
        	sensitivity=1.0,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "length")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.mac_burst_tagger_0, 0), (self, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self, 0), (self.digital_gfsk_demod_0, 0))
        self.connect((self.digital_gfsk_demod_0, 0), (self.mac_packet_deframer_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.mac_burst_tagger_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.mac_packet_framer_0, "out", self.blocks_pdu_to_tagged_stream_0, "pdus")
        self.msg_connect(self.mac_packet_to_pdu_0, "pdu", self, "msg_out")
        self.msg_connect(self, "msg_in", self.mac_packet_framer_0, "in")


    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.set_samp_rate(self.rate)

    def get_access_code_threshold(self):
        return self.access_code_threshold

    def set_access_code_threshold(self, access_code_threshold):
        self.access_code_threshold = access_code_threshold

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        self.samps_per_sym = samps_per_sym

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

