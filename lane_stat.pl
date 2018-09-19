#!/usr/bin/perl -w
use strict;
die "perl $0 <info.csv>\n" unless @ARGV == 1;
my $info = $ARGV[0];
open IN,$info;
<IN>;
my %hash;
while(<IN>){
  chomp;
  my @arr = split/,/;
  my $key = $arr[0];
  my $value = $arr[3];
  $hash{$key} += $value;
}
close IN;
foreach my $k( sort keys %hash){
  print $k,"\t",$hash{$k},"\n";
}
