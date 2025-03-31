#!/usr/bin/perl

require 'vboxctrl-lib.pl';
&ReadParse();
init_config();

$DEBUGMODE = $config{'DEBUGMODE'};
if($DEBUGMODE)
	{
	DebugOut();
	}

my $VBOXBIN = $config{'PATH_VB_BIN'};
if (! ($VBBOXBIN =~ /\/$/))
	{
	$VBOXBIN .= "/";
	}

my $VM = $in{'vm'};
my $USER = $in{'user'};
my $MODE = $in{'mode'};

if ($MODE eq "Start")
	{
	print &ui_form_start("control_vm.cgi");
	$COMMAND;
	if ($config{'multiuser'})
		{
		$COMMAND = "sudo -H -u $USER ";
		}
	$COMMAND .= $VBOXBIN."VBoxManage --nologo startvm \"$VM\" --type headless 2>&1"; #-type vrdp ";
	print "COMMAND_kab: $COMMAND <br>";
	if ($DEBUGMODE)
		{
		print "COMMAND_kab: $COMMAND <br>";
		}
	print "<b>ERROR_kab:$USER</b><br>";
	my $RETURN = readpipe($COMMAND);


	print "<center><font size='+1' color='red'><b>Control VM '$VM'</b></font><br><br>";
	print " ";
	if ($RETURN =~ /error/gi)
		{
		print "VM \"$VM\" start with Error";
		}
	else
		{
		print "VM \"$VM\" started";
		}

#	print &ui_submit($text{'butt_vmstart'}, "StartVM");
	print &ui_form_end();
	}

if ($MODE eq "Stop")
	{

	my (@STOPMODE) = ("pause","resume","reset","poweroff","savestate","acpipowerbutton");
#	my ($USER,$VM,$MODE) = @_;
	$MODE = 5;
	my $COMMAND;
	if ($config{'multiuser'})
		{
		$COMMAND = "sudo -H -u $USER ";
		}
	$COMMAND .= $VBOXBIN."VBoxManage --nologo controlvm \"$VM\" $STOPMODE[$MODE] 2>&1";
	$RETURN = readpipe($COMMAND);
	if ($DEBUGMODE)
		{
		print "COMMAND: $COMMAND - RETURN: $RETURN<br>";
		}
	if ($RETURN =~ /error/gi)
		{
		print "Stop VM with Error";
		}
	else
		{
		print  "Stop VM";
		}
	webmin_log($ACTION,$STOPMODE[$MODE],"'$VM' ($USER)",\%in);
}

	# Ruecksprung zur anfordernden Seite
		print ui_print_footer("index.cgi?mode=vm", $text{'index_return'});
