from handler.imvaha import handle_imvaha_preregistro
from handler.laura import (
    actualizar_email_participante,
    handle_laura_encuesta_principal,
    handle_laura_preregistro,
)


HANDLER_REGISTRY = {
    "laura_preregistro": handle_laura_preregistro,
    "laura_encuesta_principal": handle_laura_encuesta_principal,
    "imvaha_preregistro": handle_imvaha_preregistro,
}
