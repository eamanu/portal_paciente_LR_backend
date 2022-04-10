SQL_SUMAR = """SELECT nacer.smiafiliados.id_smiafiliados,
nacer.smiafiliados.afinombre,
nacer.smiafiliados.afitipodoc,
nacer.smiafiliados.aficlasedoc,
nacer.smiafiliados.afidni,
nacer.smiafiliados.afisexo,
facturacion.prestacion.fecha_nacimiento,
facturacion.comprobante.fecha_comprobante,
facturacion.comprobante.periodo,
facturacion.prestacion.peso,
facturacion.prestacion.tension_arterial,
facturacion.prestacion.diagnostico,
facturacion.nomenclador.codigo,
facturacion.nomenclador.grupo,
facturacion.nomenclador.subgrupo,
facturacion.nomenclador.descripcion,
facturacion.nomenclador.dias_uti,
facturacion.nomenclador.dias_sala,
facturacion.nomenclador.dias_total FROM nacer.smiafiliados
LEFT JOIN facturacion.comprobante ON nacer.smiafiliados.id_smiafiliados = facturacion.comprobante.id_smiafiliados
LEFT JOIN facturacion.prestacion ON facturacion.comprobante.id_comprobante = facturacion.prestacion.id_comprobante
LEFT JOIN facturacion.nomenclador ON facturacion.prestacion.id_nomenclador = facturacion.nomenclador.id_nomenclador
LEFT JOIN facturacion.nomenclador_detalle ON facturacion.nomenclador.id_nomenclador_detalle = facturacion.nomenclador_detalle.id_nomenclador_detalle
WHERE nacer.smiafiliados.afidni = '{dni_afiliado}'"""
