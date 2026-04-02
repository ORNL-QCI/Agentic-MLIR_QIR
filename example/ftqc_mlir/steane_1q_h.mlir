module @steane_1q_h {
  func.func @steane_1q_h() -> i1 {
    %lq = ftqc.init_zero : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %h  = ftqc.logical_h %lq : !ftqc.logical_qubit<#ftqc.ecc<steane, 3>>
    %b  = ftqc.logical_measure %h : (!ftqc.logical_qubit<#ftqc.ecc<steane, 3>>) -> i1
    func.return %b : i1
  }
}
