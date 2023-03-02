&sectionHeader('Small Examples');
$subtotal = 0;
@SOURCE = ();
@LINK = ();
$subtotal = &runTest('001', 'P2 expected wins');
$subtotal += &runTest('002', 'P2 move');
$subtotal += &runTest('003', 'P1 expected wins');
$subtotal += &runTest('004', 'P1 move');
$total += floor($subtotal);
&sectionResults('Small Examples', $subtotal, 4);
$testCount += 4;

&sectionHeader('Other examples');
$subtotal = 0;
@SOURCE = ();
@LINK = ();
$subtotal = &runTest('005', 'Initial Position');
$subtotal += &runTest('006', 'P1 Mid-game');
$subtotal += &runTest('007', 'P1 Mid-game move');
$subtotal += &runTest('008', 'P2 Start of turn');
$subtotal += &runTest('009', 'P2 nonterminal but guaranteed win');
$subtotal += &runTest('010', 'P2 with P1 max score');
$subtotal += &runTest('011', 'P2 Mid-game move');
$total += floor($subtotal);
&sectionResults('Other examples', $subtotal, 7);
$testCount += 7;

