* ============================================================
* Packages
* ============================================================
cap which reghdfe
if _rc ssc install reghdfe, replace
cap which esttab
if _rc ssc install estout, replace
cap which estadd
if _rc ssc install estout, replace

// https://texviewer.herokuapp.com/
* ============================================================
* Load + sample restrictions
* ============================================================
import delimited "C:\Users\Administrator\Desktop\jsleelab\cryptocompare\lookup\data\wp_baseline_usdkrw.csv", clear

gen double in_l0 = inflow/1e15
gen double t_l0 = totflow/1e15
gen double n_l0 = netflow/1e15
gen double out_l0 = -outflow/1e15



drop if missing(premium)
gen double pr = abs(premium)


* ============================================================
* Variables
* ============================================================

gen date_s = date(date, "YMD")
format date_s %td
// keep if date_s > td(31jan2024)
drop date
rename date_s date


egen src_id  = group(src)
egen dst_id  = group(dst)
egen pair_id = group(exchange_pair)


label var t_l0 	"Totalflow"
label var in_l0  "Inflow"
label var out_l0  "Outflow"
label var n_l0  "Netflow"
label var pr	"Premium"
label var close_fx	"FX"


levelsof network, local(netlist)
gen m = mofd(date)
format m %tm
gen y = yofd(date)




* ============================================================
* Output file (single file with panels)
* ============================================================
local OUT "baseline_panels.tex"

eststo clear
* ============================================================
* Helper program: run models + patch OLS within R2
* ============================================================
cap prog drop run_models
prog def run_models
    syntax , TIMEFE(string) RHS(varlist) DEP(string) [FX(string)]

    local tf = lower("`timefe'")
    local time_fe = cond("`tf'"=="y","y","m")

    local tfx = lower("`fx'")
    local X ""
    if "`tfx'"=="on" local X "close_fx"

	local rhs = "`rhs'"
    local dep "`dep'"


    preserve
        if "`X'"=="" drop if missing(`dep')
        else         drop if missing(`dep', `X')
        eststo m1: reg     `dep' `rhs' `X', vce(robust)
        eststo m2: reghdfe `dep' `rhs' `X', absorb(`time_fe') vce(robust)
        drop if missing(src_id)
        eststo m3: reghdfe `dep' `rhs' `X', absorb(src_id `time_fe') vce(cluster src_id)
    restore

    preserve
        if "`X'"=="" drop if missing(`dep', dst_id)
        else         drop if missing(`dep', `X', dst_id)
        eststo m4: reghdfe `dep' `rhs' `X', absorb(dst_id `time_fe') vce(cluster dst_id)
        drop if missing(src_id)
        eststo m6: reghdfe `dep' `rhs' `X', absorb(src_id dst_id `time_fe') vce(cluster src_id dst_id)
		drop if missing(pair_id)
        eststo m5: reghdfe `dep' `rhs' `X', absorb(pair_id `time_fe') vce(cluster pair_id)
    restore

    quietly estimates restore m1
    capture estadd scalar r2_within   = e(r2)
    capture estadd scalar r2_a_within = e(r2_a)
	
	    * ---- FE indicators attach (right after models exist)
	foreach M in m1 m2 m3 m4 m5 {
		capture estimates restore `M'
		if _rc continue

		local pair ""
		local src  ""
		local dst  ""
		local time ""

		if inlist("`M'","m2","m3","m4","m5","m6") local time "Yes"
		if inlist("`M'","m3","m6")               local src  "Yes"
		if inlist("`M'","m4","m6")               local dst  "Yes"
		if "`M'"=="m5"                           local pair "Yes"

		estadd local FE_pair "`pair'", replace
		estadd local FE_src  "`src'",  replace
		estadd local FE_dst  "`dst'",  replace
		estadd local FE_time "`time'", replace

		capture estimates drop `M'
		estimates store `M'
	}
end

cap prog drop store5
prog def store5
    // usage: store5, prefix(t)
    syntax , PREFIX(name)

    eststo `prefix'_m1: estimates restore m1
    eststo `prefix'_m2: estimates restore m2
    eststo `prefix'_m3: estimates restore m3
    eststo `prefix'_m4: estimates restore m4
    eststo `prefix'_m5: estimates restore m5
end

cap prog drop run_and_store
prog def run_and_store
    // Examples:
    // run_and_store5, prefix(t)  timefe(m) fx(off) dep(pr) rhs("t_l0")
    // run_and_store5, prefix(bk_t) timefe(m) fx(off) dep(pr) rhs("t_l0") ///
    //     ifexp(src=="BITHUMB" & dst=="KRAKEN")

    syntax , PREFIX(name) TIMEFE(string) DEP(name) RHS(string asis) [FX(string) IFEXP(string asis)]

    if "`ifexp'" != "" {
        preserve
            keep if `ifexp'
            run_models, timefe(`timefe') fx(`fx') dep(`dep') rhs(`rhs')
            store5, prefix(`prefix')
        restore
    }
    else {
        run_models, timefe(`timefe') fx(`fx') dep(`dep') rhs(`rhs')
        store5, prefix(`prefix')
    }
end

cap prog drop run_specs
prog def run_specs, rclass
    // usage:
    // run_specs, timefe(m) fx(off) dep(pr)
    // run_specs, prefix(bk) timefe(m) fx(off) dep(pr)
    // run_specs, timefe(m) fx(off) dep(pr) exc(src=="BITHUMB" & dst=="KRAKEN")
    // run_specs, prefix(sub) timefe(m) fx(off) dep(pr) exc(src=="BITHUMB" & dst=="KRAKEN")

    syntax , TIMEFE(string) FX(string) DEP(name) [PREFIX(string) EXC(string asis)]

    local p "`prefix'" // normalize prefix: ensure it ends with "_" if provided
    if "`p'" != "" {
        if substr("`p'", -1, 1) != "_" local p "`p'_"
    }
    local IFCLAUSE ""
    if "`exc'" != "" local IFCLAUSE `"ifexp(`exc')"'

    run_and_store, prefix(`p't)   timefe(`timefe') fx(`fx') dep(`dep') rhs("t_l0") `IFCLAUSE'
    run_and_store, prefix(`p'io)  timefe(`timefe') fx(`fx') dep(`dep') rhs("in_l0 out_l0") `IFCLAUSE'
    run_and_store, prefix(`p'out) timefe(`timefe') fx(`fx') dep(`dep') rhs("out_l0") `IFCLAUSE'
    run_and_store, prefix(`p'in)  timefe(`timefe') fx(`fx') dep(`dep') rhs("in_l0") `IFCLAUSE'
    run_and_store, prefix(`p'n)  timefe(`timefe') fx(`fx') dep(`dep') rhs("n_l0") `IFCLAUSE'
end



* ============================================================
* Regression
* ============================================================

run_specs, timefe(m) fx(off) dep(pr) exc(`exc_pair')

local exc_pair network=="eth"
run_specs, prefix(eth) timefe(m) fx(off) dep(pr) exc(`exc_pair')

local exc_pair network=="tron"
run_specs, prefix(tron) timefe(m) fx(off) dep(pr) exc(`exc_pair')

* ============================================================
* LaTeX
* ============================================================
local NOTE_DEP "Regress the daily Bitcoin premium on the amount of transferred flow, scaled by 1,000 trillion."
local NOTE_SE  "Standard errors are clustered as indicated in each column."
local NROW_DEP  "\multicolumn{9}{l}{\footnotesize `NOTE_DEP'}\\"
local NROW_SE   "\multicolumn{9}{l}{\footnotesize `NOTE_SE'}\\"

local STATS ///
	nomtitles ///
    stats(FE_pair FE_src FE_dst FE_time N r2 r2_a, fmt(%s %s %s %s %9.0g %9.3f %9.3f) ///
          labels("Pair FE" "Korea FE" "U.S. FE" "Time FE" "Observations" "R-squared" "Adj. R-squared"))


local K_tn t_l0 n_l0 _cons
local K_io  out_l0 in_l0 _cons
local K_nio  n_l0 out_l0 in_l0 _cons
local TABOPTS_TN ///
    label se star(* 0.10 ** 0.05 *** 0.01) ///
    b(%9.4f) se(%9.4f) ///
    keep(`K_tn') order(`K_tn') ///
    `STATS'
local TABOPTS_IO ///
    label se star(* 0.10 ** 0.05 *** 0.01) ///
    b(%9.4f) se(%9.4f) ///
    keep(`K_io') order(`K_io') ///
    `STATS'
local TABOPTS_NIO ///
    label se star(* 0.10 ** 0.05 *** 0.01) ///
    b(%9.4f) se(%9.4f) ///
    keep(`K_nio') order(`K_nio') ///
    `STATS'
	
cap program drop prehead_title
program define prehead_title, rclass
    // only takes title(), uses ncols/pletter if they exist; otherwise defaults
    syntax , I(int) TITLE(string asis)
	
	local ncols 9
	local pletter = char(64 + `i') 
	local line "Panel`pletter'. `title'"
    return local prehead "\multicolumn{`ncols'}{l}{\textbf{`line'}}\\"
end



prehead_title, i(1) title("Total Flow and Netflow")
esttab t_m1 t_m2 t_m3 t_m4  n_m1 n_m2 n_m3 n_m4 using "`OUT'", replace ///
    prehead("\begin{table}[!htbp]\centering\footnotesize" ///
            "\caption{Baseline Regressions of the Absolute Value of Premium}\label{tab:flow}\toprule" ///
            "\begin{tabular}{lcccccccc}" ///
            `r(prehead)') ///	
    `TABOPTS_TN' ///
	postfoot("\midrule")

	
prehead_title, i(2) title("Inflow and Outflow")
esttab out_m3 out_m4 out_m5 in_m3 in_m4 in_m5 io_m3 io_m5  using "`OUT'", append ///
	prehead(`r(prehead)') ///	
    `TABOPTS_IO'  ///
	postfoot("\midrule")


prehead_title, i(3) title("Ethereum and Tron Network")
esttab eth_n_m5 eth_out_m5  eth_in_m5 eth_io_m5 tron_n_m5 tron_out_m5 tron_in_m5 tron_io_m5   using "`OUT'", append ///
	prehead(`r(prehead)' ///
	"&\multicolumn{4}{c}{Ethereum}&\multicolumn{4}{c}{Tron} \\" ///
	) ///	
    `TABOPTS_NIO' ///
	postfoot("\midrule" ///
			`NROW_DEP' ///
			`NROW_SE')

	
file open fh using "`OUT'", write append
file write fh "\bottomrule" _n
file write fh "\end{tabular}" _n
file write fh "\end{table}" _n
file close fh
