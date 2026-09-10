from app.application.dtos.servico_dto import ServicoResponseDTO
from app.domain.entities.servico import Servico


class ServicoMapper:
    @staticmethod
    def paraResponseDto(servico: Servico) -> ServicoResponseDTO:
        return ServicoResponseDTO(
            id=servico.id,
            nome=servico.nome,
            descricao=servico.descricao,
            duracaoMinutos=servico.duracaoMinutos,
            preco=servico.preco,
            ativo=servico.ativo,
        )
