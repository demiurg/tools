#!/usr/bin/env perl
use strict;
use warnings;

my $file;
if (not defined $ARGV[0]){
    exit();
}else{
    $file = $ARGV[0];
}

local $/=undef;
open FILE, $file;
my $string = <FILE>;
close FILE;

#$string =~ s/("\w*($\w*")/

#Classes
#$string =~ s/package\s+(\w+);/

#Functions
$string =~ s/sub\s+(\w+)\s*{\s+my\s+(.+)\s+=\s+\@_;/def $1$2:/g;

$string = block($string);

print $string;

sub block{
    my ($string) = @_;
    #Conditionals
    $string =~ s/if\s*\((.+)\)\s*{/if $1:/g;
    $string =~ s/}\s*else\s*{\s*\n/else:\n/g;
    $string =~ s/elsif/elif/g;
    
    #Arrays
    #TO DO: NOT MAKE SWALLOW ALL
    $string =~ s/\$(\w+){\$?((?:.|})+)}/$1\[$2\]/g;
    
    #Loops
    $string =~ s/foreach\s*\(keys\s+%{(.+)}\)\s*{/for item in $1:/g;
    
    #Function calls
    $string =~ s/\$(\w+)->{\$?(.+)}/$1.$2/g;
    $string =~ s/\$(\w+)->(\w+\(.*\))/$1.$2/g;
    
    #Operations
    $string =~ s/\s+eq\s+/ == /g;    
    $string =~ s/\$(\w+)\s*\.=\s*(.*);/$1 = $1 + $2;/g;
    $string =~ s/\s*\.\s*/ + /g;

    $string =~ s/\$(\w+)\s*\+=\s*(.*);/$1 = $1 + $2;/g;
    $string =~ s/\$(\w+)\s*\++\s*;/$1 = $1 + 1;/g;
    
    $string =~ s/\$(\w+)\s*=~\s*\/(.*)\//re.match("$2", $1)/g; 
    
    #$string =~ s/->/./g;
    
    #Variables
    $string =~ s/my\s+\%(\w+)\s*=\s*(.*);/$1 = $2;/g;
    $string =~ s/my\s+\@(\w+)\s*;/$1 = dict();/g;
    
    $string =~ s/my\s+\$(\w+)\s*;/$1 = None;/g;
    $string =~ s/my\s+\$(\w+)\s*=\s*(.*);/$1 = $2;/g;
    $string =~ s/\$(\w+)/$1/g;
    
    #Misc
    $string =~ s/;//g;
    $string =~ s/\n\s*}//g;  

    return $string;
}