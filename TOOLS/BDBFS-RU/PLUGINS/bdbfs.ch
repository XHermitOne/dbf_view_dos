;BDBFS specific commands and definitions
#IFDEF _BDBFS_CH
	#BREAK
#ENDIF

;No reopen current table after ini-reading
#xcommand DISABLE REOPEN => lNoReopen:=.T.

;Show the array of messages
#xcommand Okey <arr> => Alert(<arr>)

;Show the message
#xcommand SHOW WITH BELL <x> => NFind(<x>,,,,.T.)
#xcommand SHOW <x> => NFind(<x>)

#xcommand START TIMER => m->_tOld:=Seconds()

#xcommand SET METER STEP TO <nRec> => m->_Sx_Step:= <nRec>
#xcommand START METER <cMsg> => Meter(1, <cMsg>)
#xcommand SHOW METER <nCurrent> => Meter(2,,<nCurrent>)
#xcommand END METER => Meter(3)

#xcommand START INDEX <cMsg> =>	Meter(1,<cMsg>, , LastRec()),;
	_m6CondSet(, , , , Compile('Meter(2,,RECNO())'), _Sx_Step, RECNO(), ;
                    NIL, NIL, NIL, .F., .F., NIL,  .F., )
//for compatible NTX use m6_OrdCondSet()

#xcommand START SEARCH => CheckEsc(.T.),;
			  IniSearching()	//it provokes Meter(1)

#xcommand FINISH => Meter(3), OpReady()		//it says: READY

#DEFINE _BDBFS_CH
