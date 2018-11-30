#!/usr/bin/perl -w
use strict;
die "perl $0 <seq_file>\n" unless @ARGV == 1;
my $file = $ARGV[0];
open IN,$file;
open OUT,">reversed.txt";
while(<IN>){
	chomp;
	my $seq = $_;
	my $rev = reverse $seq;
	$rev =~ tr/atcgnATCGN/tagcnTAGCN/;
	print OUT reverse $rev,"\n";
}
close IN;
close OUT;
