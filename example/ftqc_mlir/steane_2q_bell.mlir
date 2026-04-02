module @steane_2q_bell {
  func.func @steane_2q_bell() -> (i1, i1) {
    %q0 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %q1 = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %h0 = ftqc.logical_h %q0 : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>

    %cn_ctrl, %cn_tgt = ftqc.logical_cnot %h0, %q1 :
      (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>, !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>)

    %m0 = ftqc.logical_measure %cn_ctrl : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1
    %m1 = ftqc.logical_measure %cn_tgt : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1

    func.return %m0, %m1 : i1, i1
  }
}
