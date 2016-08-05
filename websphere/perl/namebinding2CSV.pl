use strict;
use warnings;

my $inputFile = './namebindings.xml';
my $outputFile = './output.csv';

open(my $input, '<:encoding(UTF-8)', $inputFile) or die "Could not open file '$i                                                                                                                                                                                 nputFile' $!";
open(my $output, '>:encoding(UTF-8)', $outputFile) or die "Could not open file '                                                                                                                                                                                 $outputFile' $!";
print $output "Key, Value\n";

while (my $row = <$input>) {
  if ($row =~ /(^.*nameInNameSpace\s*=*")(\s*JNDI\/[^\/]*\/)([^"]*)(.*stringToBi                                                                                                                                                                                 nd\s*=\s*")([^"]*)(.*)/) {
    print $output "\"$3\", \"$5\"\n";
  }
}
close $output;
close $input;
print "done\n";
