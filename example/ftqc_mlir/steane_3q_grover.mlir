module @steane_3q_grover {
  func.func @steane_3q_grover() -> (i1, i1, i1) {
    %q0 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %q1 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %q2 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %h0 = ftqc.logical_h %q0 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %h1 = ftqc.logical_h %q1 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %h2 = ftqc.logical_h %q2 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %z0 = ftqc.logical_z %h0 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %z1 = ftqc.logical_z %h1 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %z2 = ftqc.logical_z %h2 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %dh0 = ftqc.logical_h %z0 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %dh1 = ftqc.logical_h %z1 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %dh2 = ftqc.logical_h %z2 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %m0 = ftqc.logical_measure %dh0 : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1
    %m1 = ftqc.logical_measure %dh1 : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1
    %m2 = ftqc.logical_measure %dh2 : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1

    func.return %m0, %m1, %m2 : i1, i1, i1
  }
}
