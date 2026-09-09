import anyio
import bcrypt

from app.application.contracts.i_unit_of_work import IUnitOfWork
from app.application.dtos.usuario_dto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.mappers.usuario_mapper import UsuarioMapper
from app.domain.entities.usuario import Usuario
from app.domain.exceptions.validacao_error import ValidacaoError


class CriarUsuarioUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, dto: CriarUsuarioDTO) -> UsuarioResponseDTO:
        async with self._uow as uow:
            if await uow.usuarios.buscarPorEmail(dto.email):
                raise ValidacaoError("E-mail já cadastrado")

            if await uow.usuarios.buscarPorCpf(dto.cpf):
                raise ValidacaoError("CPF já cadastrado")

            senhaHash = await anyio.to_thread.run_sync(
                lambda: bcrypt.hashpw(dto.senha.encode(), bcrypt.gensalt()).decode()
            )

            usuario = Usuario.criar(
                nome=dto.nome,
                email=dto.email,
                cpf=dto.cpf,
                senhaHash=senhaHash,
                tipos=dto.tipos,
            )

            salvo = await uow.usuarios.salvar(usuario)
            await uow.commit()
            return UsuarioMapper.paraResponseDto(salvo)
