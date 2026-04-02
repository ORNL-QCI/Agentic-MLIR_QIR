module @steane_3q_qft {
  func.func @steane_3q_qft() -> (i1, i1, i1) {
    %q0 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %q1 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %q2 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %h0 = ftqc.logical_h %q0 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %cz01_0, %cz01_1 = ftqc.logical_cz %h0, %q1 :
      (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>)
    %cz02_0, %cz02_2 = ftqc.logical_cz %cz01_0, %q2 :
      (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>)

    %h1 = ftqc.logical_h %cz01_1 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %cz12_1, %cz12_2 = ftqc.logical_cz %h1, %cz02_2 :
      (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>)

    %h2 = ftqc.logical_h %cz12_2 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %m0 = ftqc.logical_measure %cz02_0 : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1
    %m1 = ftqc.logical_measure %cz12_1 : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1
    %m2 = ftqc.logical_measure %h2 : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1

    func.return %m0, %m1, %m2 : i1, i1, i1
  }
}
