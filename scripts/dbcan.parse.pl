# Script by Andrew Steinberger (https://github.com/asteinberger9)

open (FILE, "3715.idba.txt");
open (TBL, "3715.idba.tbl");
open (output, ">", "3715.idba.dbCAN.parsed");
$num = 1;
$nodemark = ();
while (defined($x = <FILE>))
{
        if ($x =~ /^Query:/)
     	{
		@array = split(" ",$x);
		$nodemark{$array[1]} = $num;
        	$num++;
	}
}
$hold = ();
print output "ORF\tpredicted_protein\tFull_Seq_E-value\tCoverage\tLocation\n";
$AAcount = 0;
$CBMcount = 0;
$GTcount = 0;
$CEcount = 0;
$GHcount = 0;
$PLcount = 0;
$SLHcount = 0;
while (defined($tbl = <TBL>))
{
	@array = split(" ", $tbl);
	if ($tbl !~ /^\#/ and $hold !~ $array[2])
	{
		@cov = split("_", $array[2]);
                $covval = $cov[5];
                print output "${files}_$nodemark{$array[2]}\t$array[0]\t$array[4]\t$covval\t$array[2]\n"; 
		if ($array[0] =~ /^AA/)
		{
			$AAcount++;
		}
		if ($array[0] =~ /^CBM/)
                {
                       	$CBMcount++;
                }
		if ($array[0] =~ /^CE/)
                {
                       	$CEcount++;
		}
		if ($array[0] =~ /^GH/)
                {
                       	$GHcount++;
                }
		if ($array[0] =~ /^GT/)
                {
                       	$GTcount++;
                }
		if ($array[0] =~ /^PL/)
                {
                       	$PLcount++;
                }
		if ($array[0] =~ /^SLH/)
                {
                       	$SLHcount++;
		}
	}
	$hold = $array[2];
}
print output "AA total\t$AAcount\nCBM total\t$CBMcount\nCE total\t$CEcount\nGH total\t$GHcount\nGT total\t$GTcount\nPL total\t$PLcount\nSLH total\t$SLHcount\n";
close(FILE);
close(TBL);
close(output);