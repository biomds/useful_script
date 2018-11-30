#!/usr/bin/perl -w
use strict;
# This script is used to calculate the Scafford length,GC content,N50,N90, and reference length,reference GC content of
# a species's genome,which has a fasta format.
#=================================================================================
# by Chengchen hengbenxianfeng@163.com
# 2017/3/3 16:09
# Title get_GC_N50_N90.pl
#=================================================================================
die "perl $0 <input fasta file> <output file>\n" unless @ARGV == 2;
# step1 get Scafford length and GC content
open IN, $ARGV[0];
open OUT, ">$ARGV[1]";
my ( %hash, $key,$num_Sfd,$ref_len,$GC_all,$GC_content,@N50_90,$N50,$N90);
print OUT join("\t","Scafford","Seq_length","Num_of_A","Num_of_T","Num_of_C","Num_of_G","Num_of_N","GC_content"),"\n";
while(<IN>)
{
chomp;
my @line = split;
if (/^>/)
{
$key = $line[0];
$key =~ s/>//g;
$key = "Chr".$key if (!/[A-Za-z]/);
}
$hash{$key} .= $line[0] unless /^>/;
}
foreach $key (sort{$a cmp $b}keys %hash)
{
$num_Sfd ++;
my $sfd_length = length($hash{$key});
my $A = ($hash{$key} =~ tr/Aa//);
my $T = ($hash{$key} =~ tr/Tt//);
my $C = ($hash{$key} =~ tr/Cc//);
my $G = ($hash{$key} =~ tr/Gg//);
my $basecount = ($hash{$key} =~ tr/ATCGatcg//);
my $N = $sfd_length - $basecount;
my $GC = 100 * ($G+$C)/$basecount;
$ref_len += $sfd_length;
$GC_all += $GC;
print OUT "$key\t$sfd_length\t$A\t$T\t$C\t$G\t$N\t$GC\n";
}
$GC_content = $GC_all / $num_Sfd;
print join("\t","ref_length","ref_GC_content"),"\n";
print "$ref_len\t$GC_content\n";
close IN;
close OUT;
#step2 Get Scafford N50 and Scafford N90
open NEW, $ARGV[1]; #open in the output of step1
my ($count,%hash2,$key2,$ref_length,$len);
while(<NEW>)
{
chomp;
$count ++;
my @arr = split /\t/;
if($count >=2)
{
$key2 = $arr[0];
$hash2{$key2} = $arr[1];
$ref_length += $hash2{$key2};
}
}
my ($num_n50,$num_n90);
foreach $key2(sort {$hash2{$b} <=> $hash2{$a}}(keys %hash2))
{
$len += $hash2{$key2};
if($len >= ($ref_length * 0.5))
{
$num_n50 ++;
if($num_n50 == 1)
{
my $N50 = $hash2{$key2};
print join("\t","Scafford","N50"),"\n";
print "$key2\t$N50\n";
}
}
if($len >= ($ref_length * 0.9)) # This if is not equal to elsif,becuase thers is no transition relation between this if and the previous one.
{
$num_n90 ++;
if($num_n90 == 1)
{
  my $N90 = $hash2{$key2};
print join("\t","Scafford","N90"),"\n";
  print "$key2\t$N90\n";
}
}
}
close NEW;
