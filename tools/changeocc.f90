PROGRAM changeocc
  IMPLICIT NONE
  INTEGER, PARAMETER :: restart_unit=17,ounit=18
  INTEGER :: natom_read,nspin_read,nao_read,nset_max,nshell_max, &
             nmo,homo,lfomo,nelectron,i,ispin
  INTEGER, POINTER :: nso_info(:,:,:),nshell_info(:,:), &
                      nset_info(:),offset_info(:,:,:)
  REAL*8, POINTER  :: vecbuffer_read(:,:),evals(:),occups(:)
                      

  OPEN(UNIT=restart_unit,FILE="RESTART",FORM="UNFORMATTED")
  OPEN(UNIT=ounit,FILE="RESTART.occ",FORM="UNFORMATTED")

  READ (restart_unit) natom_read,nspin_read,nao_read,nset_max,nshell_max
  WRITE(ounit) natom_read,nspin_read,nao_read,nset_max,nshell_max

  ALLOCATE (nso_info(nshell_max,nset_max,natom_read))
  ALLOCATE (nshell_info(nset_max,natom_read))
  ALLOCATE (nset_info(natom_read))
  ALLOCATE (offset_info(nshell_max,nset_max,natom_read))
  
  READ (restart_unit) nset_info
  READ (restart_unit) nshell_info
  READ (restart_unit) nso_info
  WRITE (ounit) nset_info
  WRITE (ounit) nshell_info
  WRITE (ounit) nso_info

  DEALLOCATE(nso_info,nshell_info,nset_info,offset_info)

  ALLOCATE(vecbuffer_read(1,nao_read))

  DO ispin=1,nspin_read

     READ (restart_unit) nmo,homo,lfomo,nelectron
     WRITE(ounit) nmo,homo,lfomo,nelectron

     ALLOCATE(evals(nmo),occups(nmo))

     IF (lfomo < homo) THEN
         occups(homo)=0.0
         occups(lfomo)=1.0
     ENDIF

     READ (restart_unit) evals,occups
     WRITE(ounit) evals,occups

     DEALLOCATE(evals,occups)

     DO i=1,nmo
        READ(restart_unit) vecbuffer_read
        WRITE(ounit) vecbuffer_read
     ENDDO

  ENDDO

  DEALLOCATE(vecbuffer_read)
  
  END
