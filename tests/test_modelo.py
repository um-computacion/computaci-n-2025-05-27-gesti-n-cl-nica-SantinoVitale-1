import unittest
from datetime import datetime, timedelta
from src.modelo import (
    Paciente, Medico, Especialidad, Turno, Receta, HistoriaClinica, Clinica,
    PacienteNoEncontradoException, MedicoNoDisponibleException, TurnoOcupadoException,
    RegistroDuplicadoException, RecetaInvalidaException, EspecialidadInvalidaException
)

class TestModeloClinica(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Perez", "12345678", "01/01/1990")
        self.medico = Medico("Dra. Gomez", "M123")
        self.especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica = Clinica()
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

    def test_registro_paciente_duplicado(self):
        with self.assertRaises(RegistroDuplicadoException):
            self.clinica.agregar_paciente(Paciente("Otro", "12345678", "02/02/2000"))

    def test_registro_medico_duplicado(self):
        with self.assertRaises(RegistroDuplicadoException):
            self.clinica.agregar_medico(Medico("Otra", "M123"))

    def test_agregar_especialidad_duplicada(self):
        with self.assertRaises(RegistroDuplicadoException):
            self.medico.agregar_especialidad(Especialidad("Pediatría", ["viernes"]))

    def test_agendar_turno_ok(self):
        fecha = datetime(2025, 6, 9, 10, 0)  # lunes
        self.clinica.agendar_turno("12345678", "M123", "Pediatría", fecha)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_medico().obtener_matricula(), "M123")

    def test_agendar_turno_medico_no_atiende(self):
        fecha = datetime(2025, 6, 10, 10, 0)  # martes
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "M123", "Pediatría", fecha)

    def test_agendar_turno_duplicado(self):
        fecha = datetime(2025, 6, 9, 10, 0)  # lunes
        self.clinica.agendar_turno("12345678", "M123", "Pediatría", fecha)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("12345678", "M123", "Pediatría", fecha)

    def test_emitir_receta_ok(self):
        self.clinica.emitir_receta("12345678", "M123", ["Paracetamol"])
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_sin_medicamentos(self):
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "M123", [])

    def test_historia_clinica_paciente_no_existente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")

if __name__ == "__main__":
    unittest.main()