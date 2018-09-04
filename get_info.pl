#!/usr/bin/perl -w
##date 20180904 16:00
## 
##Discription: This script is used to calculate the reads number,sequencing length,total bases,GC content,Q20,and Q30 of a sample by a info.csv.bak file
##
use strict;
use File::Basename;
die "perl $0 <SR_path>
Example:
perl $0 /GPFS04/SRProject4/SR17211_20180830_X4_AHLJWLCCXY/L3-SR17211
" unless @ARGV == 1;
my $path = $ARGV[0];#example $path:/GPFS04/SRProject4/SR17211_20180830_X4_AHLJWLCCXY/L3-SR17211
my $info_bak = "$path/info.csv.bak";
my $out_name = basename $path;
	$out_name = $out_name.".csv";
open IN,"<$info_bak" || die;
my $head = qq/Sample ID,index,Reads,Length,Total_base(Mbases),GC(%),Q20(%),Q30(%)/;
open OUT,">$out_name" || die;
print OUT "$head\n";
my ($fq1,$read1_n,$len1,$base1_n,$GC1,$Q20_1,$Q30_1);
my ($fq2,$read2_n,$len2,$base2_n,$GC2,$Q20_2,$Q30_2);
while(<IN>){
	chomp;
	if(/^#/){
		next;
	}else{
	my @arr = split /,/;
	if(($.-4)%4 == 2){
		 ($fq1,$read1_n,$len1,$base1_n,$GC1,$Q20_1,$Q30_1) = @arr[0..6];
	}
	elsif($.%4 == 0){
		 ($fq2,$read2_n,$len2,$base2_n,$GC2,$Q20_2,$Q30_2) = @arr[0..6];
	
	my @sample_tmp = split /_/,$fq1;
	my $sample_id = $sample_tmp[0]."_".$sample_tmp[2];
	my $first_line = `less $fq1 | head -1`;
	chomp	$first_line;
	my $index_tmp = (split/\s+/,$first_line)[1];
	my $index = (split/\:/,$index_tmp)[-1];
	my $reads  = $read1_n;
	my $length = $len1;
	my $total_bases = sprintf "%.2f",($base1_n + $base2_n);
	my $GC = sprintf "%.2f",($GC1+$GC2)/2;
	my $Q20 = sprintf "%.2f",($Q20_1+$Q20_2)/2;
	my $Q30 = sprintf "%.2f",($Q30_1+$Q30_2)/2;
	print OUT join(",",$sample_id,$index,$reads,$length,$total_bases,$GC,$Q20,$Q30),"\n";
		}
	}
}



close IN;
close OUT;
