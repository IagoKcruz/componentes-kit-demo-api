from app.domain.entities.servico import Servico
from app.application.dtos.servico_dto import ServicoResponseDTO


class ServicoMapper:
    @staticmethod
    def para_response_dto(servico: Servico) -> ServicoResponseDTO:
        return ServicoResponseDTO(
            id=servico.id,
            nome=servico.nome,
            descricao=servico.descricao,
            duracao_minutos=servico.duracao_minutos,
            preco=servico.preco,
            ativo=servico.ativo,
        )
