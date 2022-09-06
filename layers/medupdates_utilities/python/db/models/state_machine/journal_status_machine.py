# import db
import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from transitions import Machine
from layers.medupdates_utilities.python.datatypes.jounrnal_status import JournalStatus
from sqlalchemy.ext.hybrid import hybrid_property

class JournalStatusMachine(Machine):
    @hybrid_property
    def status(self):
        return JournalStatus(self._status)

    @status.setter
    def status(self, state):
        if self._status != state.value:
            self._status = state.value

    transitions = [
        ['schedule', JournalStatus.Draft,JournalStatus.Scheduled],
        ['publish', [JournalStatus.Draft, JournalStatus.Scheduled], JournalStatus.Published],
        ['archive', [JournalStatus.Draft, JournalStatus.Published, JournalStatus.Scheduled], JournalStatus.Archived],
    ]  

    def initialize_state_machine(self):
        machine = Machine(
            model=self,
            states=JournalStatus,
            transitions=JournalStatusMachine.transitions,
            initial=JournalStatus(self._status),
            model_attribute='status'
        )