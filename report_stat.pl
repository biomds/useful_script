#!/usr/bin/perl -w
use strict;
die "perl $0 <report_list>\n" unless @ARGV == 1;
my $report_list = $ARGV[0];
open IN,"$report_list";
my @head = ("Lane","SampleID","Reads","Base(Gb)","Q20","Q30","GC(%)","N(%)");
print join(",",@head),"\n";
while(<IN>){
	chomp;
	my ($R1,$R2) = split;
	my ($id,$lane) = (split /_/,$R1)[0,2];
	my $r1_reads = `grep total_reads $R1 | cut -f 2`;chomp $r1_reads;
	my $r2_reads = `grep total_reads $R2 | cut -f 2`;chomp $r2_reads;
	my $r1_bases = `grep total_base $R1 | cut -f 2`;chomp $r1_bases;
	my $r2_bases = `grep total_base $R2 | cut -f 2`;chomp $r2_bases;
	my $r1_Q20 = `grep Q20 $R1 | cut -f 2`;chomp $r1_Q20;
	my $r2_Q20 = `grep Q20 $R2 | cut -f 2`;chomp $r2_Q20;
	my $r1_Q30 = `grep Q30 $R1 | cut -f 2`;chomp $r1_Q30;
	my $r2_Q30 = `grep Q30 $R2 | cut -f 2`;chomp $r2_Q30;
	my $r1_GC = `grep GC_percent $R1 | cut -f 2`;chomp $r1_GC;
	my $r2_GC = `grep GC_percent $R2 | cut -f 2`;chomp $r2_GC;
	my $r1_N = `grep N_percent $R1 | cut -f 2`;chomp $r1_N;
	my $r2_N = `grep N_percent $R2 | cut -f 2`;chomp $r2_N;
	my $total_reads = $r1_reads + $r2_reads;
	   $total_reads = $total_reads;
	my $total_bases = $r1_bases + $r2_bases ;
	   $total_bases = sprintf "%.2f",$total_bases / 1000000000;
	my $mean_Q20 = ($r1_Q20 + $r2_Q20) / 2;
	   $mean_Q20 = sprintf "%.2f",$mean_Q20;
	my $mean_Q30 = ($r1_Q30 + $r2_Q30) / 2;
	   $mean_Q30 = sprintf "%.2f",$mean_Q30;
	my $mean_GC = ($r1_GC + $r2_GC) / 2;
	   $mean_GC = sprintf "%.2f",$mean_GC;
	my $mean_N = ($r1_N + $r2_N) / 2;
	   $mean_N = sprintf "%.2f",$mean_N;
	print join(",",$lane,$id,$total_reads,$total_bases,$mean_Q20,$mean_Q30,$mean_GC,$mean_N),"\n";
}
close IN;
