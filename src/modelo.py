from datetime import datetime

# Excepciones personalizadas
class PacienteNoEncontradoException(Exception): pass
class MedicoNoDisponibleException(Exception): pass
class TurnoOcupadoException(Exception): pass
class RecetaInvalidaException(Exception): pass
class RegistroDuplicadoException(Exception): pass
class EspecialidadInvalidaException(Exception): pass

class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        if not nombre or not dni or not fecha_nacimiento:
            raise ValueError("Todos los campos de Paciente son obligatorios.")
        self.__nombre__ = nombre
        self.__dni__ = dni
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni__

    def __str__(self) -> str:
        return f"{self.__nombre__} (DNI: {self.__dni__})"

class Especialidad:
    def __init__(self, tipo: str, dias: list[str]):
        if not tipo or not dias or not isinstance(dias, list):
            raise EspecialidadInvalidaException("Especialidad y días son obligatorios.")
        self.__tipo__ = tipo
        self.__dias__ = [d.lower() for d in dias if d.strip()]
        if not self.__dias__:
            raise EspecialidadInvalidaException("Debe indicar al menos un día válido.")

    def obtener_especialidad(self) -> str:
        return self.__tipo__

    def verificar_dia(self, dia: str) -> bool:
        return dia.lower() in self.__dias__

    def __str__(self) -> str:
        dias = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Días: {dias})"

class Medico:
    def __init__(self, nombre: str, matricula: str):
        if not nombre or not matricula:
            raise ValueError("Nombre y matrícula son obligatorios.")
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__ = []

    def agregar_especialidad(self, especialidad: Especialidad):
        if any(e.obtener_especialidad().lower() == especialidad.obtener_especialidad().lower() for e in self.__especialidades__):
            raise RegistroDuplicadoException("El médico ya tiene esa especialidad.")
        self.__especialidades__.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula__

    def obtener_especialidad_para_dia(self, dia: str):
        for esp in self.__especialidades__:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades = ", ".join(str(e) for e in self.__especialidades__)
        return f"{self.__nombre__} (Matrícula: {self.__matricula__}) - Especialidades: {especialidades}"

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        if not paciente or not medico or not fecha_hora or not especialidad:
            raise ValueError("Todos los campos de Turno son obligatorios.")
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad

    def obtener_medico(self):
        return self.__medico__

    def obtener_fecha_hora(self):
        return self.__fecha_hora__

    def __str__(self) -> str:
        return f"Turno: {self.__paciente__} con {self.__medico__} - {self.__especialidad__} el {self.__fecha_hora__}"

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        if not paciente or not medico or not medicamentos or not isinstance(medicamentos, list) or not medicamentos:
            raise RecetaInvalidaException("Receta inválida: faltan datos o medicamentos.")
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = datetime.now()

    def __str__(self) -> str:
        meds = ", ".join(self.__medicamentos__)
        return f"Receta para {self.__paciente__} por {self.__medico__} el {self.__fecha__}: {meds}"

class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        if not paciente:
            raise ValueError("La historia clínica debe tener un paciente.")
        self.__paciente__ = paciente
        self.__turnos__ = []
        self.__recetas__ = []

    def agregar_turno(self, turno: Turno):
        self.__turnos__.append(turno)

    def agregar_receta(self, receta: Receta):
        self.__recetas__.append(receta)

    def obtener_turnos(self):
        return self.__turnos__[:]

    def obtener_recetas(self):
        return self.__recetas__[:]

    def __str__(self) -> str:
        turnos = "\n".join(str(t) for t in self.__turnos__)
        recetas = "\n".join(str(r) for r in self.__recetas__)
        return f"Historia clínica de {self.__paciente__}\nTurnos:\n{turnos}\nRecetas:\n{recetas}"

class Clinica:
    def __init__(self):
        self.__pacientes__ = {}
        self.__medicos__ = {}
        self.__turnos__ = []
        self.__historias_clinicas__ = {}

    def agregar_paciente(self, paciente: Paciente):
        if paciente.obtener_dni() in self.__pacientes__:
            raise RegistroDuplicadoException("El paciente ya está registrado.")
        self.__pacientes__[paciente.obtener_dni()] = paciente
        self.__historias_clinicas__[paciente.obtener_dni()] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        if medico.obtener_matricula() in self.__medicos__:
            raise RegistroDuplicadoException("El médico ya está registrado.")
        self.__medicos__[medico.obtener_matricula()] = medico

    def obtener_pacientes(self):
        return list(self.__pacientes__.values())

    def obtener_medicos(self):
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula: str):
        if matricula not in self.__medicos__:
            raise MedicoNoDisponibleException("Médico no encontrado.")
        return self.__medicos__[matricula]

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException("Paciente no encontrado.")
        if matricula not in self.__medicos__:
            raise MedicoNoDisponibleException("Médico no encontrado.")
        medico = self.__medicos__[matricula]
        paciente = self.__pacientes__[dni]
        # Validar que el médico atienda esa especialidad ese día
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        if not any(e.obtener_especialidad().lower() == especialidad.lower() and e.verificar_dia(dia_semana) for e in medico._Medico__especialidades__):
            raise MedicoNoDisponibleException("El médico no atiende esa especialidad ese día.")
        # Validar que no haya turno duplicado
        for t in self.__turnos__:
            if t.obtener_medico().obtener_matricula() == matricula and t.obtener_fecha_hora() == fecha_hora:
                raise TurnoOcupadoException("El médico ya tiene un turno en ese horario.")
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(turno)
        self.__historias_clinicas__[dni].agregar_turno(turno)

    def obtener_turnos(self):
        return self.__turnos__[:]

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException("Paciente no encontrado.")
        if matricula not in self.__medicos__:
            raise MedicoNoDisponibleException("Médico no encontrado.")
        if not medicamentos or not isinstance(medicamentos, list):
            raise RecetaInvalidaException("Debe indicar al menos un medicamento.")
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas__[dni].agregar_receta(receta)

    def obtener_historia_clinica(self, dni: str):
        if dni not in self.__historias_clinicas__:
            raise PacienteNoEncontradoException("Paciente no encontrado.")
        return self.__historias_clinicas__[dni]

    @staticmethod
    def obtener_dia_semana_en_espanol(fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]